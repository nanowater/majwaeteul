# 메인 코드
import tkinter as tk
import subprocess
import tempfile
import os

def compile_and_run():
    test_count = int(test_count_input.get())

    for i in range(test_count):
        subprocess.call(['python', 'generate_TC.py'])

        with open('INPUT.txt', 'r') as f:
            inputs = f.read()

        for name, text_widget, output_widget in [('USER_CODE', text_user_code, output_user_code), ('ANSWER_CODE', text_answer_code, output_answer_code)]:
            output_widget.delete('1.0', tk.END)

            with tempfile.NamedTemporaryFile('w', delete=False, suffix='.cc') as f:
                f.write(text_widget.get('1.0', tk.END))
                temp_name = f.name

            compile_process = subprocess.Popen(['g++', temp_name, '-o', name, '-O2', '-Wall', '-lm', '-static', '-std=gnu++17', '-DONLINE_JUDGE', '-DBOJ'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            compile_output, compile_error = compile_process.communicate()

            if compile_error:
                output_widget.insert(tk.END, f'Compile Error: {compile_error.decode()}\n')
                break
            else:
                run_process = subprocess.Popen([f'./{name}'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                run_output, run_error = run_process.communicate(inputs.encode())

                if run_error:
                    output_widget.insert(tk.END, f'Runtime Error: {run_error.decode()}\n')
                    break
                else:
                    output_widget.insert(tk.END, f'{run_output.decode()}\n')

            os.remove(temp_name)

        if output_user_code.get('1.0', tk.END) != output_answer_code.get('1.0', tk.END):
            test_status_label.config(text=f'Test {i+1}: Failed. Outputs do not match.')
            return
        else:
            test_status_label.config(text=f'Test {i+1}: Passed.')

    test_status_label.config(text='All tests passed successfully!')

root = tk.Tk()

test_status_label = tk.Label(root, text='Test status: Not started')
test_status_label.grid(row=0, column=0, columnspan=2)

text_user_code = tk.Text(root)
text_user_code.grid(row=1, column=0, sticky="nsew")

output_user_code = tk.Text(root)
output_user_code.grid(row=2, column=0, sticky="nsew")

text_answer_code = tk.Text(root)
text_answer_code.grid(row=1, column=1, sticky="nsew")

output_answer_code = tk.Text(root)
output_answer_code.grid(row=2, column=1, sticky="nsew")

test_count_input = tk.Entry(root)
test_count_input.grid(row=3, column=0)

button_run_code = tk.Button(root, text='Compile & Run Code', command=compile_and_run)
button_run_code.grid(row=3, column=1)

root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
