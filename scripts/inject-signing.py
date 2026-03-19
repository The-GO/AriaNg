#!/usr/bin/env python3
"""Inject signing config into Capacitor-generated build.gradle."""
import sys

def inject_signing(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    signing_config = '''
    signingConfigs {
        release {
            storeFile file("ariang-release.keystore")
            storePassword System.getenv("KEYSTORE_PASSWORD")
            keyAlias System.getenv("KEY_ALIAS")
            keyPassword System.getenv("KEY_PASSWORD")
        }
    }
'''

    # Insert signingConfigs before buildTypes
    if 'signingConfigs' not in content:
        content = content.replace(
            '    buildTypes {',
            signing_config + '    buildTypes {'
        )

    # Add signingConfig to release buildType
    if 'signingConfig signingConfigs.release' not in content:
        content = content.replace(
            'release {\n            minifyEnabled',
            'release {\n            signingConfig signingConfigs.release\n            minifyEnabled'
        )

    with open(filepath, 'w') as f:
        f.write(content)

    print(f"Signing config injected into {filepath}")

if __name__ == '__main__':
    inject_signing(sys.argv[1])
