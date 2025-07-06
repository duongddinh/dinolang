
import sys
import os
from lexer import Lexer
from parser import Parser
from codegen import CodeGenerator

def compile_dinolang(input_file_path):
    if not os.path.exists(input_file_path):
        print(f"Error: Input file '{input_file_path}' not found.")
        return

    if not input_file_path.endswith('.dino'):
        print(f"Error: Input file must have a '.dino' extension. Got '{input_file_path}'")
        return

    output_file_path = input_file_path.replace('.dino', '.s')

    try:
        with open(input_file_path, 'r') as f:
            text = f.read()

        lexer = Lexer(text)
        # tokens = []
        # while True:
        #     token = lexer.get_next_token()
        #     tokens.append(token)
        #     if token.type == 'EOF':
        #         break
        # print("Tokens:", tokens)

        lexer = Lexer(text)
        parser = Parser(lexer)
        ast = parser.parse()
        # print("AST:", ast)

        codegen = CodeGenerator()
        assembly_code = codegen.generate_assembly(ast)

        with open(output_file_path, 'w') as f:
            f.write(assembly_code)

        print(f"Compilation successful! Assembly code saved to '{output_file_path}'")
        print("\nTo compile and run on macOS, use the following commands in your terminal:")
        print(f"  gcc -o {output_file_path.replace('.s', '')} {output_file_path}")
        print(f"  ./{output_file_path.replace('.s', '')}")

    except Exception as e:
        print(f"Compilation failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dinoc.py <input_file.dino>")
        sys.exit(1)

    input_file = sys.argv[1]
    compile_dinolang(input_file)


