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
            v-bind:key="selectValue"
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

let bigChartMonthData = [[], [], [], []];
let bigChartYearData = [[], [], [], []];
let yearChartLabels = [
  "53 weeks ago",
  "52 weeks ago",
  "51 weeks ago",
  "50 weeks ago",
  "49 weeks ago",
  "48 weeks ago",
  "47 weeks ago",
  "46 weeks ago",
  "45 weeks ago",
  "44 weeks ago",
  "43 weeks ago",
  "42 weeks ago",
  "41 weeks ago",
  "40 weeks ago",
  "39 weeks ago",
  "38 weeks ago",
  "37 weeks ago",
  "36 weeks ago",
  "35 weeks ago",
  "34 weeks ago",
  "33 weeks ago",
  "32 weeks ago",
  "31 weeks ago",
  "30 weeks ago",
  "29 weeks ago",
  "28 weeks ago",
  "27 weeks ago",
  "26 weeks ago",
  "25 weeks ago",
  "24 weeks ago",
  "23 weeks ago",
  "22 weeks ago",
  "21 weeks ago",
  "20 weeks ago",
  "19 weeks ago",
  "18 weeks ago",
  "17 weeks ago",
  "16 weeks ago",
  "15 weeks ago",
  "14 weeks ago",
  "13 weeks ago",
  "12 weeks ago",
  "11 weeks ago",
  "10 weeks ago",
  "9 weeks ago",
  "8 weeks ago",
  "7 weeks ago",
  "6 weeks ago",
  "5 weeks ago",
  "4 weeks ago",
  "3 weeks ago",
  "2 weeks ago",
  "1 week ago",
];
let monthChartLabels = [
  "30 days ago",
  "29 days ago",
  "28 days ago",
  "27 days ago",
  "26 days ago",
  "25 days ago",
  "24 days ago",
  "23 days ago",
  "22 days ago",
  "21 days ago",
  "20 days ago",
  "19 days ago",
  "18 days ago",
  "17 days ago",
  "16 days ago",
  "15 days ago",
  "14 days ago",
  "13 days ago",
  "12 days ago",
  "11 days ago",
  "10 days ago",
  "9 days ago",
  "8 days ago",
  "7 days ago",
  "6 days ago",
  "5 days ago",
  "4 days ago",
  "3 days ago",
  "2 days ago",
  "1 day ago",
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

    activeCities.sort().push("Choose City");

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
        { name: "CO" },
        {
          name: "SO2",
        },
        { name: "O3" },
        { name: "NO2" },
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
      console.log("year:",yearRes)

      const params = ['co','so2','o3','no2']
      for(let i = 0; i<5;i++){
        try{
          bigChartYearData[i] = yearRes[params[i]].data
        } catch {
          bigChartYearData[i] = []
        }
      }

      this.initYearChart(0);
    },
    async getMonthChart(cityName) {
      let axios = this.$axios;
      const monthData = await axios.get(`/api/month/${cityName}`);
      const monthRes = monthData.data.time_month;
      console.log("month:",monthRes)

      const params = ['co','so2','o3','no2']
      for(let i = 0; i<5;i++){
        try{
          bigChartMonthData[i] = monthRes[params[i]].data
        } catch {
          bigChartMonthData[i] = []
        }
      }


      this.initMonthChart(0);
    },
    unsubscribe() {}, //Waiting to be assigned unsubscribe from created()
  },
  mounted() {
    // Gets the city from the store and creates charts
    if (this.$store.state.lastCity != "Choose City") {
      console.log("in mounted", this.$store.state.lastCity);
      this.getYearChart(this.$store.state.lastCity);
      this.getMonthChart(this.$store.state.lastCity);
    }
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
