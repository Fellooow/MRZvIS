if __name__ == '__main__':
    from constrictor import Compressor
    compressor = Compressor('images/instagram-256x256.png', 8, 8, 100, 5000)
    compressor.process()
