from server.core.data_preprocessing import extract_features as ef
from server.core.data_preprocessing import corpus as c
from server.core.data_preprocessing import classify as cl

def run(vocab_url, classifier):
    corpus_file = c.extract_corpus(vocab_url)
    vocab = ef.extract_vocab(corpus_file)
    files = ef.extract_features(vocab)
    cl.train(vocab, files[0], classifier)
    cl.validate()

if __name__ == "__main__":
    print("Choose vocab file")
    print("1. vocab.csv")
    print("2. vocab2.csv")
    vocab_choice = int(input("Enter choice:"))

    if vocab_choice==1:
        vocab_url="./server/core/data_preprocessing/vocab.csv"
    else:
        vocab_url = "./server/core/data_preprocessing/vocab2.csv"

    print("Choose classifier")
    print("1. MultinomialNB")
    print("2. RandomForestClassifier (no of tree: 110)")
    print("3. GaussianNB")  #error
    print("4. NearestCentroid")
    print("5. MLPClassifier (Neural Network)")
    classifier = int(input("Enter Classifier: "))

    run(vocab_url, classifier)