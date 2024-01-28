import tkinter as tk
import subprocess
import tempfile
import os

def compile_and_run(name, text_widget, output_widget, inputs):
    # C++ 코드를 임시 파일에 저장
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.cc') as f:
        f.write(text_widget.get('1.0', tk.END))
        temp_name = f.name

    # g++로 코드 컴파일
    compile_process = subprocess.Popen(['g++', temp_name, '-o', name, '-O2', '-Wall', '-lm', '-static', '-std=gnu++17', '-DONLINE_JUDGE', '-DBOJ'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    compile_output, compile_error = compile_process.communicate()

    # 컴파일 에러가 있는 경우
    if compile_error:
        output_widget.insert(tk.END, f'Compile Error: {compile_error.decode()}\n')
    else:
        # 컴파일된 프로그램 실행
        run_process = subprocess.Popen([f'./{name}'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 입력 값을 전달
        run_input = '\n'.join([str(i.get()) for i in inputs.values()]) + '\n'
        run_output, run_error = run_process.communicate(run_input.encode())

        # 실행 결과 또는 에러 출력
        if run_error:
            output_widget.insert(tk.END, f'Runtime Error: {run_error.decode()}\n')
        else:
            output_widget.insert(tk.END, f'Output: {run_output.decode()}\n')

    # 임시 파일 삭제
    os.remove(temp_name)

# GUI 생성
root = tk.Tk()

# 정규식 입력 텍스트 박스
regex_input = tk.Entry(root)
regex_input.grid(row=0, column=0, columnspan=2, sticky="nsew")

# 사용자 코드 입력 텍스트 박스
text_user_code = tk.Text(root)
text_user_code.grid(row=1, column=0, sticky="nsew")

# '컴파일 & 실행' 버튼
button_user_code = tk.Button(root, text='Compile & Run User Code', command=lambda: compile_and_run('USER_CODE', text_user_code, output_user_code, inputs))
button_user_code.grid(row=2, column=0)

# 사용자 코드 출력 텍스트 박스
output_user_code = tk.Text(root)
output_user_code.grid(row=3, column=0, sticky="nsew")

# 답안 코드 입력 텍스트 박스
text_answer_code = tk.Text(root)
text_answer_code.grid(row=1, column=1, sticky="nsew")

# '컴파일 & 실행' 버튼
button_answer_code = tk.Button(root, text='Compile & Run Answer Code', command=lambda: compile_and_run('ANSWER_CODE', text_answer_code, output_answer_code, inputs))
button_answer_code.grid(row=2, column=1)

# 답안 코드 출력 텍스트 박스
output_answer_code = tk.Text(root)
output_answer_code.grid(row=3, column=1, sticky="nsew")

# 입력 값 프레임
inputs_frame = tk.Frame(root)
inputs_frame.grid(row=4, column=0, columnspan=2, sticky="nsew")

# 입력 값
inputs = {}

# 그리드 셀 크기 조정
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
