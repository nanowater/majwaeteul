# 메인 코드
import tkinter as tk
import subprocess
import tempfile
import os

def compile_and_run():
    output_user_code.delete('1.0', tk.END)
    output_answer_code.delete('1.0', tk.END)

    for name, text_widget, output_widget in [('USER_CODE', text_user_code, output_user_code), ('ANSWER_CODE', text_answer_code, output_answer_code)]:
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.cc') as f:
            f.write(text_widget.get('1.0', tk.END))
            temp_name = f.name

        compile_process = subprocess.Popen(['g++', temp_name, '-o', name, '-O2', '-Wall', '-lm', '-static', '-std=gnu++17', '-DONLINE_JUDGE', '-DBOJ'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        compile_output, compile_error = compile_process.communicate()

        if compile_error:
            output_widget.insert(tk.END, f'Compile Error: {compile_error.decode()}\n')
        else:
            with open('INPUT.txt', 'r') as f:
                inputs = f.read()
            run_process = subprocess.Popen([f'./{name}'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            run_output, run_error = run_process.communicate(inputs.encode())

            if run_error:
                output_widget.insert(tk.END, f'Runtime Error: {run_error.decode()}\n')
            else:
                output_widget.insert(tk.END, f'{run_output.decode()}\n')

        os.remove(temp_name)

def generate_testcase():
    subprocess.call(['python', 'generate_TC.py'])

root = tk.Tk()

button_generate_testcase = tk.Button(root, text='Generate Testcase', command=generate_testcase)
button_generate_testcase.grid(row=0, column=0, columnspan=2)

text_user_code = tk.Text(root)
text_user_code.grid(row=1, column=0, sticky="nsew")

output_user_code = tk.Text(root)
output_user_code.grid(row=2, column=0, sticky="nsew")

text_answer_code = tk.Text(root)
text_answer_code.grid(row=1, column=1, sticky="nsew")

output_answer_code = tk.Text(root)
output_answer_code.grid(row=2, column=1, sticky="nsew")

button_run_code = tk.Button(root, text='Compile & Run Code', command=compile_and_run)
button_run_code.grid(row=3, column=0, columnspan=2)

root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
