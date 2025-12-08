import pandas as pd
import numpy as np
from pathlib import Path 
import argparse
import soundfile as sf
import matplotlib.pyplot as plt


def make_dataframe (file_path: Path) -> pd.DataFrame:
    """
    принимает csv файл с аннотацией и формирует DataFrame 
    с двумя колонками: абсолютный и относительный путь
    """
    file_path = Path(file_path)
    df = pd.read_csv(file_path)

    if df.shape[1] < 2:
        raise ValueError(f"В файле должно быть минимум две колонки, а в этом файле {df.shape[1]}")
    else:
        new_df = df.iloc[:, 1:3]
        print("Сформирован DataFrame с двумя колонками")
        return new_df

    

def name_columns (new_df: pd.DataFrame) -> pd.DataFrame:
    """
    даёт имена колонкам в DataFrame
    """
    new_df.columns = ["Absolute path", "Relative path"]
    print("Колонки получили названия Absolute path и Relative path")
    return new_df



def calculate_duration (x: pd.Series) -> float:
    """
    вычисляет длительности аудиофайлов
    """
    audio_path = x["Absolute path"]

    data, samplerate = sf.read(audio_path)
    duration = len(data)/samplerate
    return round(duration, 3)



def create_column (new_df: pd.DataFrame) -> pd.DataFrame:
    """
    создаёт новую колонку: длительности аудиофайлов
    """
    new_df['Audio duration'] = new_df.apply(calculate_duration, axis = 1)
    print("Создана колонка Audio duration с длительностями аудио файлов")
    return new_df



def sort_by_duration (new_df: pd.DataFrame) -> pd.DataFrame:
    """
    сортирует по колонке с длительностью по возрастанию
    """
    sorted_df = new_df.sort_values(["Audio duration"], ascending = True)
    sorted_df = sorted_df.reset_index(drop = True)
    print("Данные колонки Audio duration отсортированы по возрастанию")
    return sorted_df



def filter_by_duration (new_df: pd.DataFrame) -> pd.DataFrame:
    """
    фильтрует по колонке с длительностью 
    (остаются аудио больше 10 секунд и меньше 100)
    """
    filtered_df = new_df[(new_df["Audio duration"] > 10) & (new_df["Audio duration"] < 100)]
    filtered_df = filtered_df.reset_index(drop = True)
    print(f"Данные колонки Audio duration отфильтрованы, осталось {len(filtered_df)} строк")
    print(f"Неколько начальных строк: {filtered_df.head(5)}")
    return filtered_df



def make_and_save_graph (sorted_df: pd.DataFrame) -> None:
    """
    строит график по добавленной колонке для 
    отсортированных данных и сохраняет его в файл
    """

    x = np.arange(0, len(sorted_df))
    y = sorted_df["Audio duration"].values

    plt.figure(figsize=(10,5))

    plt.plot(x, y, marker='.', linestyle='-', linewidth=0.5, color='blue', label="Длительность аудио")
    plt.title('График длительностей аудио файлов')
    plt.xlabel('Индекс аудио')
    plt.ylabel('Длительность аудио')
    plt.axhline(0, color='black', linewidth=0.9, ls='--')
    plt.axvline(0, color='black', linewidth=0.9, ls='--')
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.3)
    plt.legend()
    
    filename = "audio_duration_graph.png"
    plt.savefig(filename, dpi = 300)
    plt.show()

    print(f"График сохранён как {filename}")
    return None



def save_dataframe (sorted_df: pd.DataFrame, csv_path: Path) -> None:
    """
    сохраняет DataFrame в csv файл
    """
    csv_path = Path(csv_path)
    sorted_df.to_csv(csv_path, index = False)

    print(f"DataFrame сохранён как {csv_path}")
    return None



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Путь к csv файлу с аннотацией")
    parser.add_argument("-o", "--output", type=str, help="Путь для сохранения нового csv файла")
    args = parser.parse_args()

    try:
        maked_df = make_dataframe(args.input)
        named_df = name_columns(maked_df)
        with_new_col_df = create_column(named_df)
        sort_df = sort_by_duration(with_new_col_df)
        filter_df = filter_by_duration(sort_df)
        
        make_and_save_graph(sort_df)
        save_dataframe(sort_df, args.output)
        
    except Exception as error:
        print(f"Произошла ошибка: {error}")


if __name__ == "__main__":
    main()