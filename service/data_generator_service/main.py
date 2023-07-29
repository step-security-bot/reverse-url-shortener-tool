from components.data_generator import DataGenerator

def main(): 
    global data_generator
    data_generator = DataGenerator()
    data_generator.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('#'*94, 'executor.shutdown(cancel_futures=True)\n')
        data_generator.url_manager.executor.shutdown(cancel_futures=True)
        print('*'*94, 'database.conn.close()')
        data_generator.database.conn.close()
        print('&'*94, 'Done!')
        exit()
    