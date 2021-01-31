# -*- coding: UTF-8 -*-

import os
from copy import deepcopy
from json import load, dumps
from pathlib import Path

MCMETA = {
    'pack': {
        "pack_format": 6,
        "description": "Flat biomes dimensions of Minecraft"
    }
}

DATA_FORMAT = {
    'type': 'minecraft:{type}',
    'generator': {
        'type': 'minecraft:flat',
        'settings': {
            'layers': [
                {
                    'height': 1,
                    'block': 'minecraft:{color}_stained_glass'
                }
            ],
            'biome': 'minecraft:{biome}',
            'structures': {
                'stronghold': {
                    'count': 0
                },
                'structures': {}
            }
        }
    }
}


class DataPack:
    def __init__(self, mcmeta: dict):
        self.__gen_meta(mcmeta)

    @staticmethod
    def __gen_meta(mcmeta: dict):
        with open('pack.mcmeta', 'w') as meta:
            meta.write(f'{dumps(obj=mcmeta, indent=4)}\n')


class FlatBiome(DataPack):
    def __init__(self, mcmeta: dict, data_format: dict, data: dict):
        super().__init__(mcmeta)
        self.__gen_void_dims(data_format, data)

    @staticmethod
    def __gen_void_dims(data_format: dict, data: dict):
        for namespace, types in data.items():
            if not Path(path := f'data\\{namespace}\\dimension').is_dir():
                os.makedirs(path)
            for dim_type, setting in types.items():
                for dim_id, biome in setting.get('dims', dict()).items():
                    (data_format_copy := deepcopy(data_format))['type'] = f'minecraft:{dim_type}'
                    data_format_copy['generator']['settings'].update({
                        'layers': [
                            {
                                'height': 1,
                                'block': f'minecraft:{setting.get("color", "white")}_stained_glass'
                            }
                        ],
                        'biome': f'minecraft:{biome}'
                    })
                    with open(f'data\\{namespace}\\dimension\\{dim_id}.json', 'w') as dim_data_json:
                        dim_data_json.write(f'{dumps(obj=data_format_copy, indent=4)}\n')


if __name__ == '__main__':
    with open('data.json', 'r') as data_json:
        FlatBiome(MCMETA, DATA_FORMAT, load(data_json))
