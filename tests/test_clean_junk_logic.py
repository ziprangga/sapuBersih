import os
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open
import plistlib
import pytest
from src.clean_junk_logic import JunkFileCleaner
from src.utility import ResourceManager as util


# Fixture for JunkFileCleaner
@pytest.fixture(
    scope="function"
)  # Scoped to function, creating a new JunkFileCleaner instance for each test
def junk_file_cleaner():
    ui_mock = MagicMock()  # Mock the UI
    return JunkFileCleaner(ui_mock)


# Test for 'find_files_by_pattern'
@patch(
    "pathlib.Path.rglob",
    return_value=[Path("/path/file1.txt"), Path("/path/file2.log")],
)
@patch("pathlib.Path.is_dir", return_value=True)
@patch("pathlib.Path.exists", return_value=True)
def test_find_files_by_pattern(mock_exists, mock_is_dir, mock_rglob, junk_file_cleaner):
    # Valid input with patterns
    result = junk_file_cleaner.find_files_by_pattern(["/path"], ["*.txt", "*.log"])
    assert sorted(result) == sorted(["/path/file1.txt", "/path/file2.log"])

    # Validate that mocks were called as expected
    mock_exists.assert_called()
    mock_is_dir.assert_called()
    mock_rglob.assert_called_with("*.log")  # Confirming pattern usage


# Test for edge case: Empty input to 'find_files_by_pattern'
def test_find_files_by_pattern_empty_input(junk_file_cleaner):
    result = junk_file_cleaner.find_files_by_pattern([], [])
    assert result == []  # Expecting no files for empty input


# Test for 'get_uninstalled_apps' with valid .bom files
@patch("pathlib.Path.is_dir", return_value=True)
@patch("pathlib.Path.exists", return_value=True)
@patch("src.utility.ResourceManager.receipt_paths", return_value=["/receipts"])
@patch(
    "pathlib.Path.iterdir",
    return_value=[
        MagicMock(is_file=MagicMock(return_value=True), suffix=".bom", stem="app1"),
        MagicMock(is_file=MagicMock(return_value=True), suffix=".bom", stem="app2"),
        MagicMock(is_file=MagicMock(return_value=True), suffix=".txt", stem="other"),
    ],
)
def test_get_uninstalled_apps(
    mock_receipt_paths, mock_exists, mock_is_dir, mock_iterdir, junk_file_cleaner
):
    result = junk_file_cleaner.get_uninstalled_apps()
    assert result == {"app1", "app2"}  # Expect apps identified from .bom files


# Test for 'get_uninstalled_apps' with no .bom files
@patch(
    "pathlib.Path.iterdir",
    return_value=[Path("/receipts/other.txt")],  # No .bom files present
)
@patch("pathlib.Path.is_dir", return_value=True)
@patch("pathlib.Path.exists", return_value=True)
@patch("src.utility.ResourceManager.receipt_paths", return_value=["/receipts"])
def test_get_uninstalled_apps_no_bom_files(
    mock_receipt_paths, mock_exists, mock_is_dir, mock_iterdir, junk_file_cleaner
):
    result = junk_file_cleaner.get_uninstalled_apps()
    assert result == set()  # Expect empty set when no .bom files are found

    # Validate that mocks were called
    mock_receipt_paths.assert_called_once()
    mock_iterdir.assert_called_once()


# Test for 'analyze_metadata' with a valid plist file
@patch("builtins.open", new_callable=mock_open)
@patch("plistlib.load", return_value={"CFBundleName": "TestApp"})
def test_analyze_metadata_valid(mock_plist_load, mock_file, junk_file_cleaner):
    result = junk_file_cleaner.analyze_metadata("/path/to/valid.plist")
    assert result == "TestApp", "Should extract CFBundleName from a valid plist file"

    # Validate that mocks were called as expected
    mock_file.assert_called_once_with("/path/to/valid.plist", "rb")
    mock_plist_load.assert_called_once()


# Test for 'analyze_metadata' with a plist lacking required metadata
@patch("builtins.open", new_callable=mock_open)
@patch("plistlib.load", return_value={})
def test_analyze_metadata_missing_metadata(
    mock_plist_load, mock_file, junk_file_cleaner
):
    result = junk_file_cleaner.analyze_metadata("/path/to/missing_metadata.plist")
    assert result is None, "Should return None when required metadata is missing"

    # Validate that mocks were called as expected
    mock_file.assert_called_once_with("/path/to/missing_metadata.plist", "rb")
    mock_plist_load.assert_called_once()


# Test for 'analyze_metadata' with an invalid plist file
@patch("builtins.open", new_callable=mock_open)
@patch("plistlib.load", side_effect=plistlib.InvalidFileException)
def test_analyze_metadata_invalid(mock_plist_load, mock_file, junk_file_cleaner):
    result = junk_file_cleaner.analyze_metadata("/path/to/invalid.plist")
    assert result is None, "Should return None for an invalid plist file"

    # Validate that mocks were called as expected
    mock_file.assert_called_once_with("/path/to/invalid.plist", "rb")
    mock_plist_load.assert_called_once()


# Test for 'analyze_metadata' with a non-existent file
@patch("builtins.open", side_effect=FileNotFoundError)
def test_analyze_metadata_missing_file(mock_file, junk_file_cleaner):
    result = junk_file_cleaner.analyze_metadata("/path/to/nonexistent.plist")
    assert result is None, "Should return None for a non-existent file"

    # Validate that the file open was attempted
    mock_file.assert_called_once_with("/path/to/nonexistent.plist", "rb")


# Test for 'is_protected_by_sip'
@patch(
    "src.utility.ResourceManager.sip_paths",
    return_value=[Path("/protected/path1"), Path("/protected/path2")],
)
def test_is_protected_by_sip(mock_sip_paths, junk_file_cleaner):
    # Test case when file is protected
    result_protected = junk_file_cleaner.is_protected_by_sip(
        "/protected/path1/file.txt"
    )
    assert result_protected is True, "File in protected path should return True"

    # Reset mock to ensure clean slate for next assertion
    mock_sip_paths.reset_mock()

    # Test case when file is not protected
    result_not_protected = junk_file_cleaner.is_protected_by_sip(
        "/unprotected/path/file.txt"
    )
    assert result_not_protected is False, "File in unprotected path should return False"

    # Validate that sip_paths was called once per method execution
    mock_sip_paths.assert_called_once()


# Test for when the checkbox is checked
def test_include_apple_app_checked(junk_file_cleaner):
    # Mock the UI's checkbox behavior
    junk_file_cleaner.ui.include_file_checkbox.isChecked.return_value = True

    # Call the method
    result = junk_file_cleaner.include_apple_app()

    # Assert that the result is an empty list
    assert result == [], "Should return an empty list when checkbox is checked"


# Test for when the checkbox is unchecked, and util.include_apple returns paths
@patch("src.utility.ResourceManager.include_apple", return_value={"App1", "App2"})
def test_include_apple_app_unchecked_with_paths(mock_include_apple, junk_file_cleaner):
    # Mock the UI's checkbox behavior
    junk_file_cleaner.ui.include_file_checkbox.isChecked.return_value = False

    # Call the method
    result = junk_file_cleaner.include_apple_app()

    # Assert that the result contains the mocked paths
    assert sorted(result) == [
        "App1",
        "App2",
    ], "Should return paths when include_apple provides them"

    # Ensure that include_apple was called
    mock_include_apple.assert_called_once()


# Test for when the checkbox is unchecked, and util.include_apple returns nothing
@patch("src.utility.ResourceManager.include_apple", return_value=None)
def test_include_apple_app_unchecked_no_paths(mock_include_apple, junk_file_cleaner):
    # Mock the UI's checkbox behavior
    junk_file_cleaner.ui.include_file_checkbox.isChecked.return_value = False

    # Call the method
    result = junk_file_cleaner.include_apple_app()

    # Assert that the result is an empty list
    assert result == [], "Should return an empty list when include_apple returns None"

    # Ensure that include_apple was called
    mock_include_apple.assert_called_once()


# Test for 'add_file_to_ui'
@patch("os.path.basename", side_effect=lambda x: x.split("/")[-1])
@patch("os.access", side_effect=lambda x, mode: x.endswith("1.txt"))
def test_add_file_to_ui(mock_os_access, mock_os_basename, junk_file_cleaner):
    # Mock the UI's add_tree_item method
    junk_file_cleaner.ui.add_tree_item = MagicMock()

    # Test data
    files = ["/path/to/file1.txt", "/path/to/file2.log"]
    category = "documents"

    # Call the method
    junk_file_cleaner.add_file_to_ui(files, category)

    # Assert that add_tree_item was called with the correct parameters
    junk_file_cleaner.ui.add_tree_item.assert_any_call(
        "file1.txt", "/path/to/file1.txt", category, True
    )
    junk_file_cleaner.ui.add_tree_item.assert_any_call(
        "file2.log", "/path/to/file2.log", category, False
    )


# Test for 'scan_files'
@patch(
    "src.clean_junk_logic.JunkFileCleaner.is_protected_by_sip",
    side_effect=lambda x: "/protected/" in x,
)
@patch(
    "src.clean_junk_logic.JunkFileCleaner.find_files_by_pattern",
    return_value=[
        "/path/file1.txt",
        "/path/protected/file2.log",
        "/path/app_file.plist",
        "/path/other_file.tmp",
    ],
)
@patch(
    "src.clean_junk_logic.JunkFileCleaner.analyze_metadata",
    side_effect=lambda x: "UninstalledApp" if "app_file" in x else None,
)
def test_scan_files(
    mock_analyze_metadata, mock_find_files, mock_is_protected, junk_file_cleaner
):
    # Test data
    scan_path = ["/path"]
    patterns = ["*.txt", "*.log", "*.plist", "*.tmp"]
    included_apps = ["InstalledApp"]
    uninstalled_apps = {"UninstalledApp"}

    # Call the method
    result = junk_file_cleaner.scan_files(
        scan_path, patterns, included_apps, uninstalled_apps
    )

    # Expected files: 'file1.txt' (not SIP-protected and not excluded),
    # 'app_file.plist' (related to uninstalled app), 'other_file.tmp' (generic junk)
    expected_files = ["/path/file1.txt", "/path/app_file.plist", "/path/other_file.tmp"]

    # Assertions
    assert sorted(result) == sorted(
        expected_files
    ), "scan_files should return only valid junk files"

    # Ensure that mocks were called
    mock_find_files.assert_called_once_with(scan_path, patterns)
    mock_is_protected.assert_any_call("/path/file1.txt")
    mock_is_protected.assert_any_call("/path/protected/file2.log")
    mock_analyze_metadata.assert_any_call("/path/app_file.plist")
    mock_analyze_metadata.assert_any_call("/path/other_file.tmp")


# Test for 'scan_junk_files'
@patch(
    "src.clean_junk_logic.JunkFileCleaner.scan_files",
    side_effect=[
        ["/temp/file1.tmp", "/temp/file2.tmp"],  # Temporary Files
        ["/cache/file1.cache"],  # Cache Files
        ["/prefs/file1.pref"],  # Preference Files
        ["/logs/file1.log"],  # Log Files
        ["/app_support/file1.app"],  # Application Support Files
    ],
)
@patch("src.clean_junk_logic.JunkFileCleaner.include_apple_app", return_value=[])
@patch(
    "src.clean_junk_logic.JunkFileCleaner.get_uninstalled_apps",
    return_value={"UninstalledApp"},
)
@patch(
    "src.utility.ResourceManager.patterns_generals",
    return_value=["*.tmp", "*.cache", "*.log", "*.app"],
)
@patch("src.utility.ResourceManager.patterns_pref", return_value=["*.pref"])
@patch("src.utility.ResourceManager.app_support_paths", return_value=["/app_support"])
@patch("src.utility.ResourceManager.log_paths", return_value=["/logs"])
@patch("src.utility.ResourceManager.temp_paths", return_value=["/temp"])
@patch("src.utility.ResourceManager.cache_paths", return_value=["/cache"])
@patch("src.utility.ResourceManager.preference_paths", return_value=["/prefs"])
def test_scan_junk_files(
    mock_pref_paths,
    mock_cache_paths,
    mock_temp_paths,
    mock_log_paths,
    mock_app_support_paths,
    mock_patterns_pref,
    mock_patterns_generals,
    mock_uninstalled_apps,
    mock_include_apple,
    mock_scan_files,
    junk_file_cleaner,
):
    # Mock the UI methods
    junk_file_cleaner.ui.clear_tree = MagicMock()
    junk_file_cleaner.ui.show_question = MagicMock(return_value=True)
    junk_file_cleaner.ui.include_file_checkbox.isChecked = MagicMock(return_value=True)
    junk_file_cleaner.ui.include_file_checkbox.setChecked = MagicMock()
    junk_file_cleaner.add_file_to_ui = MagicMock()

    # Call the method
    result = junk_file_cleaner.scan_junk_files()

    # Expected result: combined list of all files returned by scan_files
    expected_result = [
        "/temp/file1.tmp",
        "/temp/file2.tmp",
        "/cache/file1.cache",
        "/prefs/file1.pref",
        "/logs/file1.log",
        "/app_support/file1.app",
    ]

    # Assertions
    assert sorted(result) == sorted(
        expected_result
    ), "scan_junk_files should return all found files"

    # Ensure the UI methods were called as expected
    junk_file_cleaner.ui.clear_tree.assert_called_once()
    junk_file_cleaner.ui.show_question.assert_called_once_with(
        "Are you sure to include Apple applications?"
    )
    junk_file_cleaner.ui.include_file_checkbox.isChecked.assert_called_once()

    # Check specific calls to add_file_to_ui
    junk_file_cleaner.add_file_to_ui.assert_any_call(
        ["/temp/file1.tmp", "/temp/file2.tmp"], "Temporary Files"
    )
    junk_file_cleaner.add_file_to_ui.assert_any_call(
        ["/cache/file1.cache"], "Cache Files"
    )
    junk_file_cleaner.add_file_to_ui.assert_any_call(
        ["/prefs/file1.pref"], "Preference Files"
    )
    junk_file_cleaner.add_file_to_ui.assert_any_call(["/logs/file1.log"], "Log Files")
    junk_file_cleaner.add_file_to_ui.assert_any_call(
        ["/app_support/file1.app"], "Application Support Files"
    )
