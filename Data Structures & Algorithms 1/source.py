import pandas as pd

from typing import (
    Dict,
    List,
    Tuple
)

import warnings
warnings.filterwarnings('ignore')


class Source:
    def __init__(self) -> None:
        self.path = 'file_with_numbers.csv'  # nome do arquivo csv
        self.batch_nr = 0
        self.last_read_id = 0

    def update_batch_nr(self):    
        self.batch_nr += 1  # atualiza o batch number
        print(f'Batch number updated to: {self.batch_nr}.')
        
    def update_last_searched_id(self, new_id):
        self.last_read_id = new_id  # atualiza o ultimo id lido
        print(f'Last id read updated to: {self.last_read_id}.')
        
    def load_state(self, batch_size) -> Dict[int, List]:
        file: pd.DataFrame = pd.read_csv(self.path)  # lê o arquivo csv
        file_size: int = len(file['number'])
        if self.last_read_id < file_size:
            upper_limit: int = self.last_read_id + batch_size
            if upper_limit >= file_size:
                upper_limit = file_size
                batch: List = list(
                    file['number'][self.last_read_id:]
                )
                return (upper_limit, batch)
            else:
                batch: List = list(
                    file['number'][self.last_read_id:upper_limit]
                )
            return (upper_limit, batch)
        return None
                