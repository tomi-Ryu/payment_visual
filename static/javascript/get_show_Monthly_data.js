const url = location.href;
const calendar_Element = document.getElementById("calendar");
const error_Show_Element = document.getElementById("error");
const chart_Element = document.getElementById('Chart');
const graph_Instead_Element = document.getElementById('graph_Instead');
const detail_Element = document.getElementById('detail');
const kind_RadioButton_List = document.getElementsByName("data_kind");
const how_Many_Kinds = kind_RadioButton_List.length;
let chart = null;

function get_show_Monthly_data() {
  // カレンダーの選択値を整形
  let YYYY_hyphen_MM = calendar_Element.value;
  let YYYYMM = YYYY_hyphen_MM.substr(0,4) + YYYY_hyphen_MM.substr(5,2);
  // 選択されたラジオボタンを探索
  let kind_Number;
  for (let i = 0; i < how_Many_Kinds; i++){
    if (kind_RadioButton_List.item(i).checked){
      kind_Number = kind_RadioButton_List.item(i).value;
      break;
    }
  }

  /* 
    グラフ再描画の際に必要な処置。
    テンプレートデータを返さないまま確定支払額データを再度リクエストする前にリクエスト前グラフデータを消す。
  */
  if (chart){
    chart.destroy();
  }

  // データ表示初期状態
  graph_Instead_Element.innerHTML = "Loading Data";
  detail_Element.innerHTML = "Loading Data";
  error_Show_Element.innerHTML = "";

  // カレンダーとラジオボタンの状況に対応するデータを取得し、適切に表示させる。
  fetch(`${url}graph_detail_Monthly_data/${YYYYMM}/${kind_Number}`).then(res => {
    if (!res.ok) {
      // エラー扱い。エラーメッセージのみ表示。
      graph_Instead_Element.innerHTML = "";
      detail_Element.innerHTML = "";
      error_Show_Element.innerHTML = `Error Response: ${res.status}`;
    } else {
      res.json().then(graph_And_Detail => {
        graph = graph_And_Detail["graph"];
        detail = graph_And_Detail["detail"];

        // graphデータ表示。ステータスが正常の時、graphデータがある場合とない場合がある。
        if (graph){
          paymentTarget = graph["paymentTarget"];
          cost = graph["cost"];
          color = graph["color"];

          if (paymentTarget.length === 0){
            graph_Instead_Element.innerHTML = "No Data";
            graph_Instead_Element.style.color = "white";
          } else {
            graph_Instead_Element.innerHTML = "";
            // chart.jsの機能はcdnから読み込まれる。
            chart = new Chart(chart_Element, {
              type: 'doughnut',
              data: {
                labels: paymentTarget,
                datasets: [{
                  label: 'Cost',
                  data: cost,
                  backgroundColor: color,
                  hoverOffset: 10
                }]
              },
              options: {
                plugins: {
                  legend: {
                    labels: {
                      color: 'white'
                    }
                  }
                }
              }
            });
          }     
        } else {
          graph_Instead_Element.innerHTML = "No Data";
          graph_Instead_Element.style.color = "white";
        }

        // detailデータ表示
        if (detail.length === 0){
          detail_Element.innerHTML = "No Data";
          detail_Element.style.color = "white";
        } else {
          //// テーブルデータ作成
          // テーブル凡例の定義
          const headersByKind = {
            "1": ["日付", "利用対象", "金額"],
            "2": ["利用対象", "金額"]
          };

          // 文字列の表示において右側の列と連続しないようにスペースを設ける。ex) 家賃150000→家賃 150000
          const column_left_Space = "10px";

          // 既存の内容をクリア
          detail_Element.innerHTML = "";

          // テーブル要素を作成
          const table = document.createElement("table");
          table.style.borderCollapse = "collapse";
          table.style.marginTop = "20px";
          table.style.marginLeft = "auto";
          table.style.marginRight = "auto";

          // ヘッダー行の作成
          const headerRow = document.createElement("tr");
          headersByKind[kind_Number].forEach(headerText => {
            const th = document.createElement("th");
            th.textContent = headerText;
            th.style.color = "white";
            th.style.paddingLeft = column_left_Space;
            headerRow.appendChild(th);
          });
          table.appendChild(headerRow);

          // データ行の作成
          detail.forEach(rowData => {
            const row = document.createElement("tr");
            rowData.forEach(cellData => {
              const td = document.createElement("td");
              const displayText = cellData === null ? "---" : String(cellData);
              td.textContent = displayText;
              td.style.color = "white";
              td.style.paddingLeft = column_left_Space;
              row.appendChild(td);
            });
            table.appendChild(row);
          });

          // テーブルをDOMに追加
          detail_Element.appendChild(table);
        }    
      });
    }
  }).catch(error => {
    // エラー扱い。エラーメッセージのみ表示。
    graph_Instead_Element.innerHTML = "";
    detail_Element.innerHTML = "";
    error_Show_Element.innerHTML = `${error}`;
    error_Show_Element.style.color = "white";
  });
}

// イベントリスナー登録
window.addEventListener("load", get_show_Monthly_data);
calendar_Element.addEventListener("change", get_show_Monthly_data);
for (let i = 0; i < how_Many_Kinds; i++){
  kind_RadioButton_List.item(i).addEventListener("change", get_show_Monthly_data);
}