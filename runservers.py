import os
import multiprocessing

if __name__ == '__main__':
    backend_thread = multiprocessing.Process(name='backend_process', target=os.system('python NeptuneWeb/manage.py runserver'))
    frontend_thread = multiprocessing.Process(name='frontend_process', target=os.system('cd frontend;npm start'))
    backend_thread.start()
    frontend_thread.start()