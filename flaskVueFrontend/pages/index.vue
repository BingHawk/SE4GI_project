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
          :value="$store.state.lastCity"
          @change="$store.commit('setCity', $event.target.value)"
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
import { mapState } from "vuex";

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
let monthChartLabels = [
  1,
  2,
  3,
  4,
  5,
  6,
  7,
  8,
  9,
  10,
  11,
  12,
  13,
  14,
  15,
  16,
  17,
  18,
  19,
  20,
  21,
  22,
  23,
  24,
  25,
  26,
  27,
  28,
  29,
  30,
];
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
let missedCities = [
  "Alfonsine",
  "Bergamo",
  "Brescia",
  "Carpi",
  "Cento",
  "Cesena",
  "Civitavecchia",
  "Colorno",
  "Como",
  "Cremona",
  "Faenza",
  "Fiorano Modenese",
  "Forli'",
  "Guastalla",
  "Imola",
  "Jolanda Di Savoia",
  "Langhirano",
  "Lecco",
  "Lodi",
  "Lugagnano Val D'Arda",
  "Mantova",
  "Mezzani",
  "Milano",
  "Mirandola",
  "Molinella",
  "Monza E Della Brianza",
  "Ostellato",
  "Pavia",
  "Porretta Terme",
  "San Clemente",
  "San Lazzaro Di Savena",
  "San Leo",
  "Sassuolo",
  "Savignano Sul Rubicone",
  "Sogliano Al Rubicone",
  "Sondrio",
  "Sorbolo",
  "Varese",
  "Verucchio",
  "Villa Minozzo",
];

export default {
  name: "dashboard",
  components: {
    LineChart,
  },
  ///query the cities and visualize it on map as single items then add each to a DDL///
  async asyncData({ $axios }) {
    // console.log("asyncData running");
    const cities = await $axios.get("/api/cities");
    let activeCities = cities.data.cities;

    activeCities = activeCities.filter((city) => !missedCities.includes(city));

    return {
      selectValues: activeCities,
    };
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
        { name: "Co" },
        {
          name: "So2",
        },
        { name: "O3" },
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
    //Queries data and creates charts.
    async getYearChart(cityName) {
      let axios = this.$axios;
      const yearData = await axios.get(`/api/year/${cityName}`);
      const yearRes = yearData.data.time_year;

      bigChartYearData[0] = yearRes[Object.keys(yearRes)[0]].data;
      bigChartYearData[1] = yearRes[Object.keys(yearRes)[1]].data;
      bigChartYearData[2] = yearRes[Object.keys(yearRes)[2]].data;

      this.initYearChart(0);
    },
    async getMonthChart(cityName) {
      let axios = this.$axios;
      const monthData = await axios.get(`/api/month/${cityName}`);
      const monthRes = monthData.data.time_month;

      bigChartMonthData[0] = monthRes[Object.keys(monthRes)[0]].data;
      bigChartMonthData[1] = monthRes[Object.keys(monthRes)[1]].data;
      bigChartMonthData[2] = monthRes[Object.keys(monthRes)[2]].data;

      this.initMonthChart(0);
    },
    unsubscribe() {}, //Waiting to be assigned unsubscribe from created()
  },
  mounted() {
    // Gets the city from the store and creates charts
    console.log("in mounted", this.$store.state.lastCity);
    this.getYearChart(this.$store.state.lastCity);
    this.getMonthChart(this.$store.state.lastCity);
  },
  created() {
    //Makes the page listen to the store and update charts when store changes
    this.unsubscribe = this.$store.subscribe((setCity, state) => {
      console.log("from subscribe", state.lastCity);
      this.getYearChart(state.lastCity);
      this.getMonthChart(state.lastCity);
    });
  },
  beforeDestroy() {
    console.log("in beforeDestroy");
    // Stops listening to the store when page is left.
    this.unsubscribe();
  },
};
</script>
<style></style>
