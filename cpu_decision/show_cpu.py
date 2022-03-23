import subprocess

family_id = subprocess.check_output("lscpu | grep 'CPU family:' | awk '{print$3}'", shell=True, stderr=subprocess.STDOUT).decode().split('\n')[0]
model_id = subprocess.check_output("lscpu | grep 'Model:' | awk '{print$2}'", shell=True, stderr=subprocess.STDOUT).decode().split('\n')[0]
model_name = subprocess.check_output("lscpu | grep 'Model name:' | awk '{for(i=3;i<=NF;++i)printf $i ""FS; print""}'", shell=True, stderr=subprocess.STDOUT).decode().split('Model name:')[0]


def print_result():
    global family_id, model_id, model_name
    cpu = decide_cpu()
    print("This cpu is " + cpu + " series")
    print('CPU Family: ' + family_id)
    print('Model: ' + model_id)
    print('Model name: ' + model_name)


def decide_cpu():
    global family_id, model_id
    if family_id == '6' and model_id == '85':
        return 'skl_sp'
    elif family_id == '6' and model_id == '106':
        return 'icx_sp'
    elif family_id == '6' and model_id == '108':
        bdf = subprocess.check_output("lspci | grep 345b | grep 1e.3 | awk '{print $1}'", shell=True, stderr=subprocess.STDOUT).decode().split('\n')[0]
        cmd = 'lspci -s ' + bdf + " -xxxx | grep 90 | awk '{print $6}'"
        proc = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()   # get 94th offset
        digit = proc[0]                            # get first digit
        binary = "{0:04b}".format(int(digit))      # convert digit to 4 bit binary
        result = binary[:2]                        # get first two bit
        if result == "10":
            return("icx_d HCC")
        elif result == "00":
            return("icx_d LCC")

def main():
    print_result()


if __name__ == "__main__":
    main()
