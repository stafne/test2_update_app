#!/usr/bin/env python3
"""
Test script to verify update mechanism works
"""

import requests
import json

def test_github_api():
    # Test with a known public repository
    test_url = "https://api.github.com/repos/microsoft/vscode/releases/latest"
    
    print("Testing with Microsoft VSCode repository...")
    try:
        response = requests.get(test_url, timeout=10)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Latest release: {data.get('tag_name', 'No tag')}")
            print("✅ GitHub API is working correctly")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_your_repo():
    # Test with your repository
    your_url = "https://api.github.com/repos/stafne/test2_update_app/releases/latest"
    
    print("\nTesting with your repository...")
    try:
        response = requests.get(your_url, timeout=10)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Latest release: {data.get('tag_name', 'No tag')}")
            print("✅ Your repository is accessible")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Testing GitHub API connectivity...\n")
    
    # Test with known working repo
    if test_github_api():
        # Test with your repo
        test_your_repo()
    else:
        print("❌ Basic GitHub API test failed - check your internet connection")
