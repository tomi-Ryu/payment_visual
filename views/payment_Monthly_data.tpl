% rebase('base.tpl', for_Cache_Buster=for_Cache_Buster)
<link rel="stylesheet" href="../static/scss_css/get_show_Monthly_data.css?t={{for_Cache_Buster}}" type="text/css">

<div class="entire_container">

  <div id="error">
  </div>


  <input type="month" id="calendar" min="2024-01" max="2099-12" value="{{YYYY_hyphen_MM}}" />
  <div>
    <input type="radio" id="orig" name="data_kind" value="1" checked required/>
    <label for="orig">orig</label>
    <input type="radio" id="grp" name="data_kind" value="2" />
    <label for="grp">grp</label>
  </div>

  <div class="graph_And_Detail">
    <div id="graph">
      <div id="graph_Instead"></div>
      <canvas id="Chart"></canvas>
    </div>

    <div id="detail">
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.min.js"></script>

  <script src="../static/javascript/get_show_Monthly_data.js?t={{for_Cache_Buster}}"></script>

</div>