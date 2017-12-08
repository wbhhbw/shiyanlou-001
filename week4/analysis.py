import json
import pandas as pd

def analysis(file, user_id):
    times = 0
    minutes = 0
    try:
        df = pd.read_json(file)
        times = df[df['user_id'] == user_id]['user_id'].count()
        minutes = df[df['user_id'] == user_id]['minutes'].sum()
    except Exception:
        print('Error')
    finally:
        return times, minutes

def main():
    print(analysis('/home/shiyanlou/Code/user_study.json', 445315))

if __name__ == '__main__':
    main()