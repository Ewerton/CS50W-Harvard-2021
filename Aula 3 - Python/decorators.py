# Uma função que recebe uma função como parametro e retorna uma versão modificada desta mesma função
# Ou seja, recebe uma função por parametro, adiciona comportamentos à esta função e retorna ela.
# Isso é programação funcional onde função são tratados como valores
def announce(f):  # a função principal que recebe outra função "f" como parametro
    def wrapper():  # uma função que "envelopa" a função "f()"
        print("about to run a function...")  # comportamento adicionado
        f()  # ececuta a propria "f()" que veio por parametro
        print("Done with the function.")  # comportamento adicionado
    return wrapper  # retorna a função com comportamento modificado para o chamador


@announce  # adiciona o decorator annouce na função hello()
def hello():
    print("Hello, world!")


# só chama hello() para ver que o comportamento dela foi sobrecarregado.
hello()

# neste exemplo, a função hello() é passada por parametro para o decorator announce()
# dentro do decorator, quando "f()" é chamado, na verdade o "hello()" é executado

# Decorator são uma ferramenta poderosa.
# Você pode por exemplo criar um decorator que verifica se o usuário esta logado e somente se estiver logado executa a função recebida por parametro.
