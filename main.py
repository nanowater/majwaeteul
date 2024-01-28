import tkinter as tk
import subprocess
import tempfile
import os

def compile_and_run():
    # C++ 코드를 임시 파일에 저장
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.cpp') as f:
        f.write(text.get('1.0', tk.END))
        temp_name = f.name

    # g++로 코드 컴파일
    compile_process = subprocess.Popen(['g++', temp_name, '-o', 'temp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    compile_output, compile_error = compile_process.communicate()

    # 컴파일 에러가 있는 경우
    if compile_error:
        output.insert(tk.END, f'Compile Error: {compile_error.decode()}\n')
    else:
        # 컴파일된 프로그램 실행
        run_process = subprocess.Popen(['./temp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        run_output, run_error = run_process.communicate()

        # 실행 결과 또는 에러 출력
        if run_error:
            output.insert(tk.END, f'Runtime Error: {run_error.decode()}\n')
        else:
            output.insert(tk.END, f'Output: {run_output.decode()}\n')

    # 임시 파일 삭제
    os.remove(temp_name)

# GUI 생성
root = tk.Tk()

# 코드 입력 텍스트 박스
text = tk.Text(root)
text.pack()

# '컴파일 & 실행' 버튼
button = tk.Button(root, text='Compile & Run', command=compile_and_run)
button.pack()

# 출력 텍스트 박스
output = tk.Text(root)
output.pack()

root.mainloop()
