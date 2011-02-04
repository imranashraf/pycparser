import sys
from pycparser.c_ast import *
from pycparser.c_parser import CParser, Coord, ParseError
from pycparser.c_lexer import CLexer


def expand_decl(decl):
    """ Converts the declaration into a nested list.
    """
    typ = type(decl)
    
    if typ == TypeDecl:
        return ['TypeDecl', expand_decl(decl.type)]
    elif typ == IdentifierType:
        return ['IdentifierType', decl.names]
    elif typ == ID:
        return ['ID', decl.name]
    elif typ in [Struct, Union]:
        decls = [expand_decl(d) for d in decl.decls or []]
        return [typ.__name__, decl.name, decls]
    else:        
        nested = expand_decl(decl.type)
    
        if typ == Decl:
            if decl.quals:
                return ['Decl', decl.quals, decl.name, nested]
            else:
                return ['Decl', decl.name, nested]
        elif typ == Typename: # for function parameters
            if decl.quals:
                return ['Typename', decl.quals, nested]
            else:
                return ['Typename', nested]
        elif typ == ArrayDecl:
            dimval = decl.dim.value if decl.dim else ''
            return ['ArrayDecl', dimval, nested]
        elif typ == PtrDecl:
            return ['PtrDecl', nested]
        elif typ == Typedef:
            return ['Typedef', decl.name, nested]
        elif typ == FuncDecl:
            if decl.args:
                params = [expand_decl(param) for param in decl.args.params]
            else:
                params = []
            return ['FuncDecl', params, nested]

#-----------------------------------------------------------------

if __name__ == "__main__":    
    source_code = """
    int main()
    {
        const union blahunion tt = {
            .joe = {0, 1},
            .boo.bar[2] = 4};
        p++;
        int a;
    }
    """

    source_code = """
    int main() {
        int foo, bar;;;
        float sdf;
    }
    """

    #--------------- Lexing 
    #~ from pycparser.portability import printme
    #~ def errfoo(msg, a, b):
        #~ printme(msg)
        #~ sys.exit()
    #~ clex = CLexer(errfoo, lambda t: False)
    #~ clex.build()
    #~ clex.input(source_code)
    
    #~ while 1:
        #~ tok = clex.token()
        #~ if not tok: break
            
        #~ printme([tok.value, tok.type, tok.lineno, clex.filename, tok.lexpos])

    #--------------- Parsing
    parser = CParser()
    ast = parser.parse(source_code)

    ast.show()

