from pathlib import Path
import subprocess

save_folder = Path("/mnt/c/Users/L-G/OneDrive/Desktop/Games") #this is where it saves the .sh files
save_folder.mkdir(parents=True, exist_ok=True)  # make sure folder exists

BANNED_KEYWORDS =[
    "unitycrashhandler32",
    "unitycrashhandler64",
    "svends",
    "wallpaper32",
    "installer",
    "gaijin_downloader",# these are Crossout exe's
    "gjagent",#
    "bpreport"#
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
    for folder in folders.rglob(".exe"):
        for files in folder.iterdir():
            if files.is_file() and files.suffix == ".exe":
                if any(keyword in files.name.lower() for keyword in BANNED_KEYWORDS):
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
        if "Epic\\ Games/" in str(folder):
            games_exe = Get_Epic_Files(folder)
            return games_exe
        
        for game_exe in folder.iterdir():
            if game_exe.is_file() and game_exe.suffix == ".exe":
                if any(keyword in game_exe.name.lower() for keyword in BANNED_KEYWORDS):
                    continue
                games_exe.append(game_exe)
    return games_exe
            

def file_to_sh(game_exe : list) -> None:
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