const input = document.getElementById("file_path");
const fileName = document.getElementById("file-name");
const errorMsg = document.getElementById("file-error");

// ファイル選択時の処理
input.addEventListener("change", () => {
  const file = input.files[0];
  fileName.textContent = file ? file.name : "";
  errorMsg.classList.add("hidden"); // エラー非表示
});

// フォーム送信時のチェック
document.querySelector("form").addEventListener("submit", (e) => {
  if (!input.files.length) {
    e.preventDefault(); // 送信を止める
    errorMsg.classList.remove("hidden"); // エラー表示
  }
});
