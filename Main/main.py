from Net.netProcessor import NetProcessor

if __name__ == "__main__":
    generations = 100
    iterations = 30
    processor = NetProcessor()
    processor.run(generations, iterations)
