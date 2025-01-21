from dataclasses import dataclass
from enum import Enum

class TetrominoType(Enum):
    I = 1
    O = 2
    T = 3
    S = 4
    Z = 5
    J = 6
    L = 7

@dataclass
class Tetromino:
    shape_type: TetrominoType
    color: tuple[int, int, int]
    matrix: list[list[int]]
    x: int = 0  # 追加
    y: int = 0  # 追加
    
    @classmethod
    def create(cls, shape_type: TetrominoType):
        shapes = {
            TetrominoType.I: {
                "color": (0, 255, 255),
                "matrix": [
                    [0,0,0,0],
                    [1,1,1,1],
                    [0,0,0,0],
                    [0,0,0,0]
                ]
            },
            TetrominoType.O: {
                "color": (255, 255, 0),
                "matrix": [
                    [2,2],
                    [2,2]
                ]
            },
            TetrominoType.T: {
                "color": (128, 0, 128),
                "matrix": [
                    [0,3,0],
                    [3,3,3],
                    [0,0,0]
                ]
            },
            TetrominoType.S: {
                "color": (0, 255, 0),
                "matrix": [
                    [0,4,4],
                    [4,4,0],
                    [0,0,0]
                ]
            },
            TetrominoType.Z: {
                "color": (255, 0, 0),
                "matrix": [
                    [5,5,0],
                    [0,5,5],
                    [0,0,0]
                ]
            },
            TetrominoType.J: {
                "color": (0, 0, 255),
                "matrix": [
                    [6,0,0],
                    [6,6,6],
                    [0,0,0]
                ]
            },
            TetrominoType.L: {
                "color": (255, 165, 0),
                "matrix": [
                    [0,0,7],
                    [7,7,7],
                    [0,0,0]
                ]
            }
        }
        return cls(
            shape_type=shape_type,
            color=shapes[shape_type]["color"],
            matrix=shapes[shape_type]["matrix"],
            x=3,  # 初期位置を中央に設定
            y=0
        )
    
    def rotate(self, clockwise: bool = True):
        rotated = [list(row) for row in zip(*self.matrix[::-1])] if clockwise else [list(row) for row in zip(*self.matrix)][::-1]
        self.matrix = rotated
