from nada_dsl import *

def nada_main():
    party1 = Party(name="Party1")
    my_int1 = SecretInteger(Input(name="my_int1", party=party1))
    my_int2 = SecretInteger(Input(name="my_int2", party=party1))

    # Perform the computation with my_int1 and my_int2
    result = my_int1 + my_int2

    # Return the output with the computed result
    return [Output(result, "my_output", party1)]

# Assuming the nada_dsl framework handles the execution, inputs, and outputs,
# no need for further code outside this main function in this context.
