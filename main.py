import tkinter as tk
import subprocess
import ctypes
from tkinter import messagebox
import threading
from PIL import Image, ImageTk
import tempfile
import os
import GPUtil


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def update_vm_list():
    try:
        result = subprocess.run(["powershell", "Get-VM | Select-Object -ExpandProperty Name"], capture_output=True,
                                text=True, shell=True)

        if result.returncode != 0:
            raise Exception("Impossible d'exécuter le code PowerShell")

        vm_names = result.stdout.strip().split('\n')

        selected_vm.set("")
        vm_menu['menu'].delete(0, 'end')
        for vm_name in vm_names:
            vm_menu['menu'].add_command(label=vm_name, command=tk._setit(selected_vm, vm_name))

        root.after(60000, update_vm_list)
    except Exception as e:
        selected_vm.set("Error: " + str(e))


def show_loading_screen():
    loading_screen = tk.Toplevel(root)
    loading_screen.title("Chargement")
    loading_screen.geometry("640x428")
    loading_screen.configure(bg="black")
    loading_screen.resizable(False, False)

    loading_image = Image.open("loading_image.png")
    loading_image = ImageTk.PhotoImage(loading_image)

    loading_label = tk.Label(loading_screen, image=loading_image, bg="black")
    loading_label.image = loading_image
    loading_label.pack(pady=20)

    selected_vm_name = selected_vm.get()

    template_script = """
    $vm = "{vm_name}"

    Add-VMGpuPartitionAdapter -VMName $vm
    Set-VMGpuPartitionAdapter -VMName $vm -MinPartitionVRAM 80000000 -MaxPartitionVRAM 100000000 -OptimalPartitionVRAM 100000000 -MinPartitionEncode 80000000 -MaxPartitionEncode 100000000 -OptimalPartitionEncode 100000000 -MinPartitionDecode 80000000 -MaxPartitionDecode 100000000 -OptimalPartitionDecode 100000000 -MinPartitionCompute 80000000 -MaxPartitionCompute 100000000 -OptimalPartitionCompute 100000000

    Set-VM -GuestControlledCacheTypes $true -VMName $vm
    Set-VM -LowMemoryMappedIoSpace 1Gb -VMName $vm
    Set-VM –HighMemoryMappedIoSpace 32GB –VMName $vm
    """

    modified_script = template_script.replace("{vm_name}", selected_vm_name)

    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".ps1") as temp_file:
        temp_file.write(modified_script)
        temp_script_path = temp_file.name

    def execute_powershell_script():
        result_code = subprocess.call(["powershell.exe", "-File", temp_script_path])

        loading_screen.destroy()

        if result_code == 0:
            messagebox.showinfo("Code complété", "Le premier code PowerShell s'est exécuté avec succès.")
        else:
            messagebox.showerror("Erreur de code", "Le premier code PowerShell n'as pas correctement fonctionné.")

        os.remove(temp_script_path)

    threading.Thread(target=execute_powershell_script).start()


def show_loading_screen2():
    loading_screen = tk.Toplevel(root)
    loading_screen.title("Chargement")
    loading_screen.geometry("640x428")
    loading_screen.configure(bg="black")
    loading_screen.resizable(False, False)

    loading_image = Image.open("loading_image.png")
    loading_image = ImageTk.PhotoImage(loading_image)

    loading_label = tk.Label(loading_screen, image=loading_image, bg="black")
    loading_label.image = loading_image
    loading_label.pack(pady=20)

    selected_vm_name = selected_vm.get()

    template_script = """
    $vm = "{vm_name}"
    $systemPath = "C:\Windows\System32\"
    $driverPath = "C:\Windows\System32\DriverStore\FileRepository\"
    
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    if( $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator) ) {
        
        Get-VM -Name $vm | Get-VMIntegrationService | ? {-not($_.Enabled)} | Enable-VMIntegrationService -Verbose
        
        $localDriverFolder = ""
        Get-ChildItem $driverPath -recurse | Where-Object {$_.PSIsContainer -eq $true -and $_.Name -match "nv_dispi.inf_amd64_*"} | Sort-Object -Descending -Property LastWriteTime | select -First 1 |
        ForEach-Object {
            if ($localDriverFolder -eq "") {
                $localDriverFolder = $_.Name                                  
                }
        }
    
        Write-Host $localDriverFolder
    
        Get-ChildItem $driverPath$localDriverFolder -recurse | Where-Object {$_.PSIsContainer -eq $false} |
        Foreach-Object {
            $sourcePath = $_.FullName
            $destinationPath = $sourcePath -replace "^C\:\\Windows\\System32\\DriverStore\\","C:\Temp\System32\HostDriverStore\"
            Copy-VMFile $vm -SourcePath $sourcePath -DestinationPath $destinationPath -Force -CreateFullPath -FileSource Host
        }
    
        Get-ChildItem $systemPath  | Where-Object {$_.Name -like "NV*"} |
        ForEach-Object {
            $sourcePath = $_.FullName
            $destinationPath = $sourcePath -replace "^C\:\\Windows\\System32\\","C:\Temp\System32\"
            Copy-VMFile $vm -SourcePath $sourcePath -DestinationPath $destinationPath -Force -CreateFullPath -FileSource Host
        }
    
        Write-Host "Success! Please go to C:\Temp and copy the files where they are expected within the VM."
    
    } else {
        Write-Host "This PowerShell Script must be run with Administrative Privileges or nothing will work."
    }
    """

    modified_script = template_script.replace("{vm_name}", selected_vm_name)

    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".ps1") as temp_file:
        temp_file.write(modified_script)
        temp_script_path = temp_file.name

    def execute_powershell_script2():
        result_code = subprocess.call(["powershell.exe", "-File", temp_script_path])

        loading_screen.destroy()

        if result_code == 0:
            messagebox.showinfo("Code complété", "Le deuxième code PowerShell s'est exécuté avec succès.")
        else:
            messagebox.showerror("Erreur de code", "Le deuxième code PowerShell n'as pas correctement fonctionné.")

        os.remove(temp_script_path)

    threading.Thread(target=execute_powershell_script2).start()


def show_loading_screen3():
    loading_screen = tk.Toplevel(root)
    loading_screen.title("Chargement")
    loading_screen.geometry("640x428")
    loading_screen.configure(bg="black")
    loading_screen.resizable(False, False)

    loading_image = Image.open("loading_image.png")
    loading_image = ImageTk.PhotoImage(loading_image)

    loading_label = tk.Label(loading_screen, image=loading_image, bg="black")
    loading_label.image = loading_image
    loading_label.pack(pady=20)

    selected_vm_name = selected_vm.get()

    template_script = """
    $vm = Get-VM "{vm_name}"
    Remove-VMGpuPartitionAdapter -VM $vm
    """

    modified_script = template_script.replace("{vm_name}", selected_vm_name)

    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".ps1") as temp_file:
        temp_file.write(modified_script)
        temp_script_path = temp_file.name

    def execute_powershell_script3():
        result_code = subprocess.call(["powershell.exe", "-File", temp_script_path])

        loading_screen.destroy()

        if result_code == 0:
            messagebox.showinfo("Code complété", "Le troisième code PowerShell s'est exécuté avec succès.")
        else:
            messagebox.showerror("Erreur de code", "Le troisième code PowerShell n'as pas correctement fonctionné.")

        os.remove(temp_script_path)

    threading.Thread(target=execute_powershell_script3).start()


def get_gpu_model():
    try:
        gpu_info = GPUtil.getGPUs()[0]
        return gpu_info.name
    except Exception as e:
        return "GPU Introuvable"


root = tk.Tk()
root.title("AlibaBASH - Hyper-V GPU Paravirtualisation (PRE-ALPHA)")
root.geometry("720x360")
root.configure(bg="black")
root.resizable(False, False)

gpu_model = get_gpu_model()
title_label = tk.Label(root, text=f"Modèle du GPU : {gpu_model}", font=("Helvetica", 16), fg="white", bg="black")
title_label.pack(pady=10)

selected_vm = tk.StringVar()

vm_menu = tk.OptionMenu(root, selected_vm, "Chargement des VMs...")
vm_menu.pack(pady=20)

execute_button = tk.Button(root, text="SPLIT LE GPU", command=show_loading_screen, bg="white", fg="black")
execute_button.pack(pady=10)

execute_button2 = tk.Button(root, text="COPIER LES PILOTES DU GPU (EN COURS DE DÉVELOPPEMENT)", command=show_loading_screen2,
                            bg="white", fg="black")
execute_button2.pack(pady=10)

execute_button3 = tk.Button(root, text="Retirer le GPU", command=show_loading_screen3, bg="white", fg="black")
execute_button3.pack(pady=10)

if not is_admin():
    messagebox.showerror("Erreur", "Privilèges d'administrateur requis.")
    root.destroy()

update_vm_list()

root.mainloop()
