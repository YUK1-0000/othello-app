YAJU, KUSAI = "810", "931"

def f(input_: str):
    match input_:
        case YAJU:
            print("yaju")
        case KUSAI:
            print("kusai")

while True:
    f(input())