% rebase('base.tpl')
<div id="error">

</div>

<input type="month" id="calendar" min="2024-01" max="2099-12" value="{{YYYY_hyphen_MM}}" />
<div>
  <input type="radio" id="orig" name="data_kind" value="1" checked required/>
  <label for="orig">orig</label>
  <input type="radio" id="grp" name="data_kind" value="2" />
  <label for="grp">grp</label>
</div>


<div id="graph" style="width: 500px;">
  <div id="graph_Instead"></div>
  <canvas id="Chart"></canvas>
</div>

<div id="detail">
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.min.js"></script>

<script src="../static/javascript/get_show_Monthly_data.js?t={{for_Cache_Buster}}"></script>
