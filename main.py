# 메인 코드
import subprocess
import os
import concurrent.futures
import generate_TC
import comparing_txt
import shutil

def compile_and_run(i):
    generate_TC.generate_test_case(i)

    with open(f'generated_datas/INPUT{i}.txt', 'r') as f:
        inputs = f.read()

    for name in ['USER_CODE', 'ANSWER_CODE']:
        code_file = f'{name}.cc'
        executable_name = f'{name}_{i}'

        compile_process = subprocess.Popen(['g++', code_file, '-o', f'generated_datas/{executable_name}', '-O2', '-Wall', '-lm', '-static', '-std=gnu++17', '-DONLINE_JUDGE', '-DBOJ'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        compile_output, compile_error = compile_process.communicate()


        if compile_error:
            print(f'Compile Error: {compile_error.decode()}\n')
            return f'Test {i+1}: Failed. Compile error.'
        else:
            run_process = subprocess.Popen([f'generated_datas/{executable_name}'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            run_output, run_error = run_process.communicate(inputs.encode())


            with open(f'generated_datas/OUTPUT_{executable_name}.txt', 'w') as f:
                f.write(run_output.decode())

            if run_error:
                print(f'Runtime Error: {run_error.decode()}\n')
                return f'Test {i+1}: Failed. Runtime error.'                

    if comparing_txt.compare_files(f'generated_datas/OUTPUT_USER_CODE_{i}.txt',f'generated_datas/OUTPUT_ANSWER_CODE_{i}.txt'):
        return f'Test {i+1}: Failed. Outputs do not match.'
    else:
        return f'Test {i+1}: Passed.'

def run_tests():
    shutil.rmtree('generated_datas')
    os.mkdir('generated_datas')
    thread_count = int(input('Enter the number of threads: '))
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        results = list(executor.map(compile_and_run, range(thread_count)))

    for result in results:
        if 'Failed' in result:
            print(result)
            return

    print('All tests passed successfully!')

run_tests()
