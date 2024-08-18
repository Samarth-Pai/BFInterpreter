# Project started by Samarth Pai on 18/08/2024
import sys
from collections import defaultdict
from typing import Self

class heap:
    def __init__(self):
        self.memoryHeap = defaultdict(int)
        self.pointer = 0
    
    def __add__(self,other: int) -> Self:
        self.memoryHeap[self.pointer]+=other
        return self

    def __sub__(self,other: int) -> Self:
        self.memoryHeap[self.pointer]-=other
        return self

    @property
    def value(self) -> int:
        return self.memoryHeap[self.pointer]
    
    def __lshift__(self,other: int) -> None:
        self.pointer-=other

    def __rshift__(self,other: int) -> None:
        self.pointer+=other

    def __getitem__(self,val: int):
        self.memoryHeap[self.pointer] = val

def getBlock(code: str,idx: int)-> str:
    loopLevel = 0
    output = ""
    for c in code[idx:]:
        if c=="[":
            if loopLevel:
                output+=c
            loopLevel+=1
        elif c=="]":
            loopLevel-=1
            if loopLevel==0:
                return output
            output+=c
        else:
            output+=c
    return ""

def traceback(code: str) -> None:
    loopNumber = 0
    for en,c in enumerate(code):
        if c=="[":
            loopNumber+=1
        elif c=="]":
            if loopNumber==0:
                raise SyntaxError(f"Closing a loop which has'nt open in character number {en+1}")
            loopNumber-=1
    if loopNumber:
        raise SyntaxError("Forgot to close loop")

def interpret(code: str,h: heap=heap(),loopLevel: int=0) -> None:
    i = 0
    lenn = len(code)
    try:
        while i<lenn:
            match code[i]:
                case "+":
                    h+=1
                case "-":
                    h-=1
                case "<":
                    h<<1
                case ">":
                    h>>1
                case ".":
                    print(chr(h.value),end="",flush=True)
                case ",":
                    char = sys.stdin.read(1)
                    h[ord(char[-1])]
                case "[":
                    block = getBlock(code,i)
                    blockLen = len(block)
                    while h.value:
                        interpret(block,h,loopLevel+1)
                    i+=blockLen+1
            i+=1
        
    except KeyboardInterrupt:
        exit()

if __name__=="__main__":
    sysArgs = sys.argv
    try:
        targetFile = sysArgs[1]
        with open(targetFile) as f:
            code = f.read()
        traceback(code)
        interpret(code)
    except IndexError:
        raise Exception("Target file not supplied")