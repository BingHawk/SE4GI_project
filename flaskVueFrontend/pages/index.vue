<template>
  <div class="row">
    <!-- Big Chart -->
    <div class="col-12">
      <div
        class="btn-group btn-group-toggle"
        :class="isRTL ? 'float-left' : 'float-right'"
        data-toggle="buttons"
      >
        <select
          class="custom-select m-1  text-white w-100"
          name="Cities"
          id="idCitiesDDL"
          @change="onChange($event)"
          data-toggle="tooltip"
          title="Your destination city"
          style="
                background-image: linear-gradient(
                    45deg,
                    transparent 50%,
                    white 50%
                  ),
                  linear-gradient(135deg, white 50%, transparent 50%),
                  linear-gradient(to right, #242424, #242424);
                background-position: calc(100% - 20px) calc(1em + 2px),
                  calc(100% - 15px) calc(1em + 2px), 100% 0;
                background-size: 5px 5px, 5px 5px, 2.5em 2.5em;
                background-repeat: no-repeat;
                background-color: #41B883;
              "
        >
          <option
            v-for="selectValue in selectValues"
            :value="selectValue"
            v-bind:key="option"
            >{{ selectValue }}</option
          >
        </select>
      </div>
      <card type="chart">
        <template slot="header">
          <div class="row">
            <div class="col-sm-6" :class="isRTL ? 'text-right' : 'text-left'">
              <!-- <h5 class="card-category">Total shipments</h5> -->
              <h2 class="card-title">Monthly Data</h2>
            </div>
            <div class="col-sm-6 d-flex d-sm-block">
              <div
                class="btn-group btn-group-toggle"
                :class="isRTL ? 'float-left' : 'float-right'"
                data-toggle="buttons"
              >
                <label
                  v-for="(option, index) in bigLineChartCategories"
                  :key="option.name"
                  class="btn btn-sm btn-primary btn-simple"
                  :class="{ active: monthBigLineChart.activeIndex === index }"
                  :id="index"
                >
                  <input
                    type="radio"
                    @click="initMonthChart(index)"
                    name="options"
                    autocomplete="off"
                    :checked="monthBigLineChart.activeIndex === index"
                  />
                  <span class="d-none d-sm-block">{{ option.name }}</span>
                  <span class="d-block d-sm-none">
                    <i :class="option.icon"></i>
                  </span>
                </label>
              </div>
            </div>
          </div>
        </template>

        <div class="chart-area">
          <line-chart
            style="height: 100%"
            ref="monthBigChart"
            :chart-data="monthBigLineChart.chartData"
            :gradient-colors="monthBigLineChart.gradientColors"
            :gradient-stops="monthBigLineChart.gradientStops"
            :extra-options="monthBigLineChart.extraOptions"
          >
          </line-chart>
        </div>
      </card>
    </div>

    <div class="col-12">
      <card type="chart">
        <template slot="header">
          <div class="row">
            <div class="col-sm-6" :class="isRTL ? 'text-right' : 'text-left'">
              <h2 class="card-title">Annual Data</h2>
            </div>
            <div class="col-sm-6 d-flex d-sm-block">
              <div
                class="btn-group btn-group-toggle"
                :class="isRTL ? 'float-left' : 'float-right'"
                data-toggle="buttons"
              >
                <label
                  v-for="(option, index) in bigLineChartCategories"
                  :key="option.name"
                  class="btn btn-sm btn-primary btn-simple"
                  :class="{ active: yearBigLineChart.activeIndex === index }"
                  :id="index"
                >
                  <input
                    type="radio"
                    @click="initYearChart(index)"
                    name="options"
                    autocomplete="off"
                    :checked="yearBigLineChart.activeIndex === index"
                  />
                  <span class="d-none d-sm-block">{{ option.name }}</span>
                  <span class="d-block d-sm-none">
                    <i :class="option.icon"></i>
                  </span>
                </label>
              </div>
            </div>
          </div>
        </template>
        <div class="chart-area">
          <line-chart
            style="height: 100%"
            ref="yearBigChart"
            :chart-data="yearBigLineChart.chartData"
            :gradient-colors="yearBigLineChart.gradientColors"
            :gradient-stops="yearBigLineChart.gradientStops"
            :extra-options="yearBigLineChart.extraOptions"
          >
          </line-chart>
        </div>
      </card>
    </div>
  </div>
</template>
<script>
import LineChart from "@/components/Charts/LineChart";
import BarChart from "@/components/Charts/BarChart";
import * as chartConfigs from "@/components/Charts/config";
import TaskList from "@/components/Dashboard/TaskList";
import config from "@/config";
import { Table, TableColumn } from "element-ui";

let bigChartMonthData = [[], [], []];
let bigChartYearData = [[], [], []];
let yearChartLabels = [
  "JAN",
  "FEB",
  "MAR",
  "APR",
  "MAY",
  "JUN",
  "JUL",
  "AUG",
  "SEP",
  "OCT",
  "NOV",
  "DEC",
];
let monthChartLabels=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
let bigChartDatasetOptions = {
  fill: true,
  borderColor: config.colors.primary,
  borderWidth: 2,
  borderDash: [],
  borderDashOffset: 0.0,
  pointBackgroundColor: config.colors.primary,
  pointBorderColor: "rgba(255,255,255,0)",
  pointHoverBackgroundColor: config.colors.primary,
  pointBorderWidth: 20,
  pointHoverRadius: 4,
  pointHoverBorderWidth: 15,
  pointRadius: 4,
};
var store="firenze"


export default {
  name: "dashboard",
  components: {
    LineChart,
  },
  ///query the cities and visualize it on map as single items then add each to a DDL///
  async asyncData({ $axios, $store }) {
    // console.log("asyncData running");
    $store = (typeof $store !== 'undefined') ?  $store : "firenze"
    var cityName=$store
    console.log(cityName);
    

    const [cities, monthData, yearData] = await Promise.all([
      $axios.get("/api/cities"),
      $axios.get(`/api/month/${cityName}`),
      $axios.get(`/api/year/${cityName}`),
    ]);

    // console.log(yearData.data);
    
    const monthRes = monthData.data.time_month;
    const yearRes = yearData.data.time_year;

    bigChartMonthData[0] = monthRes.co.data;
    bigChartMonthData[1] = monthRes.so2.data;
    bigChartMonthData[2] = monthRes.o3.data;

    bigChartYearData[0] = yearRes.co.data;
    bigChartYearData[1] = yearRes.so2.data;
    bigChartYearData[2] = yearRes.o3.data;

    return {
      // data: monthData.data.time_month.co,
      // city: cities.data,
      selectValues: cities.data.cities,
    };
    // },
  },
  creatCitiesDDL() {},
  data() {
    return {
      monthBigLineChart: {
        activeIndex: 0,
        chartData: {
          datasets: [
            {
              ...bigChartDatasetOptions,
              data: bigChartMonthData[0],
            },
          ],
          labels: monthChartLabels,
        },
        extraOptions: chartConfigs.purpleChartOptions,
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.4, 0],
        categories: [],
      },
      yearBigLineChart: {
        activeIndex: 0,
        chartData: {
          datasets: [
            {
              ...bigChartDatasetOptions,
              data: bigChartYearData[0],
            },
          ],
          labels: yearChartLabels,
        },
        extraOptions: chartConfigs.purpleChartOptions,
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.4, 0],
        categories: [],
      },
    };
  },
  computed: {
    enableRTL() {
      return this.$route.query.enableRTL;
    },
    isRTL() {
      return this.$rtl.isRTL;
    },
    bigLineChartCategories() {
      return [
        { name: "Co", icon: "tim-icons icon-single-02" },
        {
          name: "So2",
          icon: "tim-icons icon-gift-2",
        },
        { name: "O3", icon: "tim-icons icon-tap-02" },
      ];
    },
  },
  methods: {
    initMonthChart(index) {
      let chartData = {
        datasets: [
          {
            ...bigChartDatasetOptions,
            data: bigChartMonthData[index],
          },
        ],
        labels: monthChartLabels,
      };
      this.$refs.monthBigChart.updateGradients(chartData);
      this.monthBigLineChart.chartData = chartData;
      this.monthBigLineChart.activeIndex = index;
      
    },

    initYearChart(index) {
      let chartData = {
        datasets: [
          {
            ...bigChartDatasetOptions,
            data: bigChartYearData[index],
          },
        ],
        labels: yearChartLabels,
      };
      this.$refs.yearBigChart.updateGradients(chartData);
      this.yearBigLineChart.chartData = chartData;
      this.yearBigLineChart.activeIndex = index;
    },
    async onChange(event){
    console.log(event.target.value)
    //this.$nuxt.refresh()
   let cityName=event.target.value
   let $axios=this.$axios
   const [ monthData, yearData] = await Promise.all([
      $axios.get(`/api/month/${cityName}`),
      $axios.get(`/api/year/${cityName}`),
    ]);

    // console.log(yearData.data);
    
    const monthRes = monthData.data.time_month;
    const yearRes = yearData.data.time_year;

    bigChartMonthData[0] = monthRes.co.data;
    bigChartMonthData[1] = monthRes.so2.data;
    bigChartMonthData[2] = monthRes.o3.data;

    bigChartYearData[0] = yearRes.co.data;
    bigChartYearData[1] = yearRes.so2.data;
    bigChartYearData[2] = yearRes.o3.data;
  }
  },
  mounted() {
    this.initMonthChart(0);
    this.initYearChart(0)
    
    
  },
 
};
</script>
<style></style>
