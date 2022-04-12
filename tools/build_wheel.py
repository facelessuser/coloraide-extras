"""Download necessary wheels and build the `coloraide` wheel."""
import sys
import subprocess
import os
import urllib.request
import urllib.error
import glob
import shutil
import re
import hashlib

# Notebook specific wheels
NOTEBOOK_WHEELS = [
    "https://files.pythonhosted.org/packages/6e/33/1ae0f71395e618d6140fbbc9587cc3156591f748226075e0f7d6f9176522/Markdown-3.3.4-py3-none-any.whl",  # noqa: E501
    "https://files.pythonhosted.org/packages/9a/9a/36f71797fbaf1f4b6cb8debe1ab6d3ec969e8dbc651181f131a16b794d80/pymdown_extensions-9.0-py3-none-any.whl",  # noqa: E501
]

# Wheels required in addition to the current project
PLAYGROUND_WHEELS = [
    "https://files.pythonhosted.org/packages/1d/17/ed4d2df187995561b28f1073df24137cb750e12f9879d291cc8ab67c65d2/Pygments-2.11.2-py3-none-any.whl",  # noqa: E501
    "https://files.pythonhosted.org/packages/6d/61/e2f04ad470b7eb312e3ad2d3dcc70150be2dc6d4789d0ee3c0bf5018e56e/coloraide-0.15.0.post1-py3-none-any.whl"  # noqa: E501
]

MKDOCS_YML = 'mkdocs.yml'

RE_CONFIG = re.compile(r'playground-config.*?\.js')
RE_BUILD = re.compile(r'Successfully built ([-_0-9.a-zA-Z]+?\.whl)')

CONFIG = """\
var color_notebook = {{
    "playground_wheels": {},
    "notebook_wheels": {},
    "default_playground": "from coloraide_extras import Color\\ncoloraide.__version__\\nColor('color(--xyy 0.64 0.33 0.21264)')"
}}
"""  # noqa: E501

OUTPUT = 'docs/src/markdown/playground/'

NOTEBOOK = {}
for url in NOTEBOOK_WHEELS:
    NOTEBOOK[os.path.join(OUTPUT, url.split('/')[-1])] = url

PLAYGROUND = {}
for url in PLAYGROUND_WHEELS:
    PLAYGROUND[os.path.join(OUTPUT, url.split('/')[-1])] = url


def build_package():
    """Build `coloraide` wheel."""
    cmd = [sys.executable, '-m', 'build', '--wheel', '-o', OUTPUT]

    if sys.platform.startswith('win'):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            startupinfo=startupinfo,
            shell=False,
            env=os.environ.copy()
        )
    else:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            shell=False,
            env=os.environ.copy()
        )
    out, _ = process.communicate()
    m = RE_BUILD.search(out.decode('utf-8'))

    return process.returncode, m.group(1) if m else ''


def download_wheel(url, dest):
    """Download a wheel."""

    print('Downloading: {}'.format(url))
    status = 0
    try:
        response = urllib.request.urlopen(url)
        status = response.status
        if status == 200:
            status = 0
            with open(dest, 'wb') as f:
                print('Writing: {}'.format(dest))
                f.write(response.read())
    except urllib.error.HTTPError as e:
        status = e.status

    if status:
        print('Failed to download, recieved status code {}'.format(status))

    return status


if __name__ == "__main__":

    status = 0

    # Clean up all old wheels
    for file in glob.glob(OUTPUT + '*.whl'):
        if file not in NOTEBOOK.keys() and file not in PLAYGROUND.keys():
            os.remove(file)

    for file in glob.glob('docs/theme/playground-config*.js'):
        os.remove(file)

    # Clean up build directory
    if os.path.exists('build'):
        shutil.rmtree('build')

    # Build wheel
    status, package = build_package()
    if not status:
        # Get dependencies
        for file, url in NOTEBOOK.items():
            if os.path.exists(file):
                print('Skipping: {}'.format(file))
                continue
            status = download_wheel(url, file)
            if status:
                break
    if not status:
        for file, url in PLAYGROUND.items():
            if os.path.exists(file):
                print('Skipping: {}'.format(file))
                continue
            status = download_wheel(url, file)
            if status:
                break

    if not status:
        # Build up a list of wheels needed for playgrounds and notebooks
        playground = [os.path.basename(x) for x in PLAYGROUND.keys()] + [package]
        notebook = [os.path.basename(x) for x in NOTEBOOK.keys()] + playground

        # Create the config that specifies which wheels need to be used
        config = CONFIG.format(str(playground), str(notebook)).replace('\r', '').encode('utf-8')
        m = hashlib.sha256()
        m.update(b'playground-config.js')
        m.update(b':')
        m.update(config)
        hsh = m.hexdigest()[0:8]
        with open('docs/theme/playground-config-{}.js'.format(hsh), 'wb') as f:
            f.write(config)

        # Update `mkdocs` source to reference wheel config
        with open(MKDOCS_YML, 'rb') as f:
            mkdocs = f.read().decode('utf-8')
        mkdocs = RE_CONFIG.sub('playground-config-{}.js'.format(hsh), mkdocs)
        with open(MKDOCS_YML, 'wb') as f:
            f.write(mkdocs.encode('utf-8'))

    print("FAILED :(" if status else "SUCCESS :)")
    sys.exit(status)
