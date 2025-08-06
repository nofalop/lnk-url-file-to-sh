from pathlib import Path
import subprocess
import re

save_folder = Path("/mnt/c/Users/L-G/OneDrive/Desktop/Games") #this is where it saves the .sh files
save_folder.mkdir(parents=True, exist_ok=True)  # make sure folder exists

BANNED_KEYWORDS = [
    "unitycrashhandler32",
    "unitycrashhandler64",
    "svends",
    "wallpaper32",
    "installer",
    "gaijin_downloader",
    "gjagent",
    "bpreport",
    "crashreportclient",
    "epicwebhelper",
    "win64",
    "uninstallhelper",
    "easyanticheat",
    "setup",
    "crashreportclient",
    "epicwebhelper"
]
files = []
#GLOBAL FILES
def Get_Files(software_path) -> list:
    directory = Path(f'{software_path}')
    for folder in directory.iterdir():
        if not folder.is_dir():
            return list() #empty list if the dir dosen't exits
        files.append(folder)
    return files

#EPIC GAMES FILES
def Get_Epic_Files(folders : Path) -> list:
    games_epic = []
    for files in folders.rglob("*.exe"):
        if not files.is_file():
            continue
        
        lowered_name = files.name.lower()
        # splits the dir if in contains - or _ then checks if it has one of the banned words
        name_parts = re.split("[-_.]", lowered_name)
        print(name_parts)
        if any(keyword in name_parts for keyword in BANNED_KEYWORDS):
            continue
        games_epic.append(files)
    return games_epic

#
def itererate_files() -> list:
    games_exe = []
    for folder_path in files:
        folder = Path(folder_path)
        if not folder.is_dir():
            continue
        
        #if the user chooses Epic games 
        if "Epic Games" in str(folder):
            return Get_Epic_Files(folder)
        
        for game_exe in folder.iterdir():
            if game_exe.is_file() and game_exe.suffix == ".exe":
                if any(keyword in game_exe.name.lower() for keyword in BANNED_KEYWORDS):
                    continue
                games_exe.append(game_exe)
            
    return games_exe
            

def file_to_sh(game_exe : list) -> None:
    if len(game_exe) <= 0:
        print("no exe files")
        return

    for game in game_exe:
        sh_name = game.stem + ".sh"
        sh_path = save_folder / sh_name
        
        # Write the exe path (or command) into the .sh file
        with open(sh_path, "w") as f:
            f.write(f'"{game}"\n')

        subprocess.run(f"chmod +x '{sh_path}'", shell=True)
    print(f"Done! Files saved to {save_folder}")

def Userinput() -> None:
    while True:
        choice : str = str(input("1-Steam\n2-Epic\npick one: ")).lower()
        match choice:
            case "steam" | "1":
                Get_Files(input("Enter Steam Games Folder Path: "))
                break
            case "epic" | "2":
                Get_Files(input("Enter Epic Games Folder Path: "))
                break
            case _:
                print("Invaid selection")

        
def main():
    Userinput()
    games = itererate_files()
    file_to_sh(games)

if __name__ == "__main__":
    main()