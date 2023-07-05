import subprocess

# Config
clone_root = r"G:\SourceCode\LearnWebGPU-Code-folded"
cherry_picked_commit = "fac8be2cff1b0d251f6bb91ded31bea5cb3bb3e3"
all_branches = [
'step020',
'step025',
'step030',
'step030-vanilla',
'step032',
'step033',
'step033-optionB',
'step034',
'step037',
'step039',
'step043',
'step044',
]
excluded_branches = [
    'main',
    'step240',
]

git = lambda *x: subprocess.run(["git", '-C', clone_root, *x], capture_output=True)

def main():
    global all_branches
    print(f"Applying commit '{cherry_picked_commit}' to all branches but " + ", ".join(excluded_branches))

    if all_branches is None:
        res = git("for-each-ref", "--format=%(refname:short)", "refs/heads/")
        all_branches = res.stdout.decode().strip().split("\n")
    res = git("show-ref", "--head", "--hash", "HEAD")
    current_head = res.stdout.decode().strip()
    
    processed_branches = []
    for branch in all_branches:
        if branch in excluded_branches:
            continue
        print(f"Processing branch '{branch}'...")
        git("checkout", branch)
        res = git("cherry-pick", cherry_picked_commit)
        if res.returncode != 0:
            print(f"Cannot cherry pick for branch '{branch}':")
            print(res.stderr.decode())
            return
        processed_branches.append(branch)

    git("checkout", current_head)
    #git("push", "origin", *processed_branches)
    print(f"Run 'git push origin {' '.join(processed_branches)}'")

main()