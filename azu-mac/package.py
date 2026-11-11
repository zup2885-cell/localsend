"""Package an independent, sandboxed ad hoc Mac development build."""
from pathlib import Path
import os
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / 'app/build/macos/Build/Products/Release/AzuQuickTransfer.app'
OUTPUT = ROOT / 'azu-mac/output'
APP = OUTPUT / '阿祖快传.app'


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if APP.exists():
        shutil.rmtree(APP)
    shutil.copytree(BUILD, APP, symlinks=True)
    resources = APP / 'Contents/Resources'
    for name in ['LICENSE', 'ADAPTATION-AZU.md']:
        shutil.copy2(ROOT / name, resources / name)
    notices = resources / 'THIRD-PARTY-LICENSES-RUST'
    notices.mkdir(exist_ok=True)
    cargo = Path(os.environ.get('CARGO_HOME', str(Path.home() / '.cargo')))
    for source in (cargo / 'registry/src').glob('*/*'):
        for file in source.rglob('*'):
            if not file.is_file():
                continue
            if not (file.name.lower().startswith(('license', 'copying', 'notice')) or 'LICENSES' in file.parts):
                continue
            target = notices / source.name / file.relative_to(source)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, target)
    swift_notices = resources / 'THIRD-PARTY-LICENSES-SWIFT'
    swift_notices.mkdir(exist_ok=True)
    checkouts = ROOT / 'app/build/macos/SourcePackages/checkouts'
    if checkouts.exists():
        for checkout in checkouts.iterdir():
            if not checkout.is_dir():
                continue
            for file in checkout.iterdir():
                if file.is_file() and file.name.lower().startswith(('license', 'copying', 'notice')):
                    target = swift_notices / checkout.name
                    target.mkdir(exist_ok=True)
                    shutil.copy2(file, target / file.name)
    for file in (ROOT / 'app/macos/Pods/Target Support Files/Pods-Runner').glob('*acknowledgements*'):
        shutil.copy2(file, swift_notices / file.name)
    (resources / 'SOURCE.txt').write_text(
        'Source: https://github.com/zup2885-cell/localsend/tree/azu-mac-1.18.2-1\n'
        'Upstream: https://github.com/localsend/localsend\n'
        'Original authors: Tien Do Nam and contributors. Apache License 2.0 is retained.\n'
        'Independent Azu adaptation. No owner files or transfer history are included.\n'
    )
    # Ad hoc packages cannot use Developer ID library validation across frameworks.
    # Keep app sandbox entitlements; do not change any host security settings.
    subprocess.run(['codesign', '--force', '--deep', '--sign', '-', '--options', '0',
                    '--preserve-metadata=entitlements', str(APP)], check=True)
    subprocess.run(['codesign', '--verify', '--deep', '--strict', str(APP)], check=True)
    print(APP)


if __name__ == '__main__':
    main()
