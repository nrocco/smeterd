<style>
    body { font-family: monospace; }
    th, td { text-align:right; }
    th:first-child, td:first-child { text-align: left; }
</style>
<table width="100%">
<tr>
    <th>date</td>
    <th>total kwh</td>
    <th>total gas</td>
    <th>kwh low</td>
    <th>kwh high</td>
    <th>gas in m3</td>
<tr/>
{% for date, total_kwh, total_gas, kwh1_min, kwh2_min, gas_min, kwh1_max, kwh2_max, gas_max in data %}
  <tr>
    <td><a href="/report/{{ date }}">{{ date }}</a></td>
      <td>{{ '%.3f'|format(total_kwh*0.001) }}</td>
      <td>{{ '%.3f'|format(total_gas*0.001) }}</td>
      <td>{{ '%.3f'|format(kwh1_max*0.001) }}</td>
      <td>{{ '%.3f'|format(kwh2_max*0.001) }}</td>
      <td>{{ '%.3f'|format(gas_max*0.001) }}</td>
  </tr>
{% endfor %}
</table>
