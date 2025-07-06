from lexer import TokenType
from parser import (
    Program, VariableDeclaration, BinaryOp, Number, Identifier,
    PrintStatement, String, InputStatement
)

class CodeGenerator:
    def __init__(self):
        self.asm, self.sym = [], {}
        self.off = 0                    # stack offset
        self.strs, self.scnt = {}, 0
        self.locals_idx = None

    def _emit(self, l): self.asm.append(l)
    def _lbl(self):     self.scnt += 1; return f"S{self.scnt}"

    def _type(self, node):
        if isinstance(node, (Number, BinaryOp)): return "int"
        if isinstance(node, String):             return "string"
        if isinstance(node, Identifier):         return self.sym[node.name][1]
        return "int"

    def _expr(self, n):
        if isinstance(n, Number):
            self._emit(f"    push ${n.value}")
        elif isinstance(n, String):
            if n.value not in self.strs: self.strs[n.value] = self._lbl()
            self._emit(f"    leaq {self.strs[n.value]}(%rip), %rax")
            self._emit( "    push %rax")
        elif isinstance(n, Identifier):
            off, vtype = self.sym[n.name]
            if vtype == "string":
                self._emit(f"    leaq {off}(%rbp), %rax")
                self._emit( "    push %rax")
            else:
                self._emit(f"    push {off}(%rbp)")
        elif isinstance(n, BinaryOp):
            self._expr(n.right); self._expr(n.left)
            self._emit("    pop %rax"); self._emit("    pop %rbx")
            op = n.op.type
            if   op == TokenType.GROW:   self._emit("    add %rbx,%rax")
            elif op == TokenType.SHRINK: self._emit("    sub %rbx,%rax")
            elif op == TokenType.HATCH:  self._emit("    imul %rbx,%rax")
            elif op == TokenType.SPLIT:  self._emit("    cqo"); self._emit("    idiv %rbx")
            else:                        raise Exception(op)
            self._emit("    push %rax")
        else:
            raise Exception(type(n))

    def _stmt(self, s):
        if isinstance(s, VariableDeclaration):     
            name = s.identifier.value
            vtype = self._type(s.expression)
            self.off -= 8; self.sym[name] = (self.off, vtype)
            self._expr(s.expression)
            self._emit("    pop %rax")
            self._emit(f"    mov %rax,{self.off}(%rbp)")

        elif isinstance(s, PrintStatement):       
            self._expr(s.expression)
            if self._type(s.expression) == "int":
                self._emit("    pop %rdi"); self._emit("    call _print_int")
            else:
                self._emit("    pop %rsi"); self._emit("    call _print_string")

        elif isinstance(s, InputStatement):       
            BUF = 256
            name = s.identifier.value
            self.off -= BUF; self.sym[name] = (self.off, "string")
            self._emit(f"    leaq {self.off}(%rbp), %rdi") 
            self._emit(f"    mov  ${BUF}, %esi")           
            self._emit("    call _input")

        else: raise Exception(type(s))

    def generate(self, tree: Program) -> str:
        self._emit(".text"); self._emit(".globl _main")

        self._emit("_print_int:")
        self._emit("    push %rbp; mov %rsp,%rbp")
        self._emit("    mov %rdi,%rsi")                
        self._emit("    leaq FMT_INT(%rip),%rdi")
        self._emit("    xor %eax,%eax"); self._emit("    call _printf")
        self._emit("    mov $0,%edi");  self._emit("    call _fflush")
        self._emit("    pop %rbp; ret\n")

        self._emit("_print_string:")
        self._emit("    push %rbp; mov %rsp,%rbp")
        self._emit("    leaq FMT_STR(%rip),%rdi")
        self._emit("    xor %eax,%eax"); self._emit("    call _printf")
        self._emit("    mov $0,%edi");  self._emit("    call _fflush")
        self._emit("    pop %rbp; ret\n")

        self._emit("_input:")                           
        self._emit("    push %rbp; mov %rsp,%rbp")
        self._emit("    movq ___stdinp@GOTPCREL(%rip), %rdx ")
        self._emit("    movq (%rdx), %rdx    ")                

        self._emit("    call _fgets")
        self._emit("    pop %rbp; ret\n")

        self._emit("_main:")
        self._emit("    push %rbp; mov %rsp,%rbp")
        self.locals_idx = len(self.asm)
        self._emit("    # patched later")

        for st in tree.statements: self._stmt(st)

        self._emit("    mov $0,%eax")
        self._emit("    leave; ret")

        size = (-self.off + 15) & ~15
        self.asm[self.locals_idx] = f"    sub ${size}, %rsp"

        self._emit("\n.data"); self._emit("    .align 8")
        for s,l in self.strs.items(): self._emit(f"{l}: .asciz \"{s}\"")
        self._emit("FMT_INT: .asciz \"%ld\\n\"")
        self._emit("FMT_STR: .asciz \"%s\\n\"")

        return "\n".join(self.asm)

    def generate_assembly(self, tree): return self.generate(tree)
