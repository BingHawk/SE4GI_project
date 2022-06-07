<template>
  <base-nav
    v-model="showMenu"
    class="navbar-absolute top-navbar"
    type="white"
    :transparent="true"
  >
    <div slot="brand" class="navbar-wrapper">
      <div
        class="navbar-toggle d-inline"
        :class="{ toggled: $sidebar.showSidebar }"
      >
        <button type="button" class="navbar-toggler" @click="toggleSidebar">
          <span class="navbar-toggler-bar bar1"></span>
          <span class="navbar-toggler-bar bar2"></span>
          <span class="navbar-toggler-bar bar3"></span>
        </button>
      </div>
      <a class="navbar-brand ml-xl-3 ml-5" href="#pablo">{{ routeName }}</a>
    </div>

    <ul class="navbar-nav" :class="$rtl.isRTL ? 'mr-auto' : 'ml-auto'">
      <!-- <div class="search-bar input-group" @click="searchModalVisible = true">
        <button
          class="btn btn-link"
          id="search-button"
          data-toggle="modal"
          data-target="#searchModal"
        >
          <i class="tim-icons icon-zoom-split"></i>
        </button>
      </div>
      <modal
        :show.sync="searchModalVisible"
        class="modal-search"
        id="searchModal"
        :centered="false"
        :show-close="true"
      >
        <input
          slot="header"
          v-model="searchQuery"
          type="text"
          class="form-control"
          id="inlineFormInputGroup"
          placeholder="SEARCH"
        />
      </modal>
      <base-dropdown
        tag="li"
        :menu-on-right="!$rtl.isRTL"
        title-tag="a"
        title-classes="nav-link"
        class="nav-item"
      >
        <template
          slot="title"
        >
          <div class="notification d-none d-lg-block d-xl-block"></div>
          <i class="tim-icons icon-sound-wave"></i>
          <p class="d-lg-none">New Notifications</p>
        </template>
        <li class="nav-link">
          <a href="#" class="nav-item dropdown-item"
            >Mike John responded to your email</a
          >
        </li>
        <li class="nav-link">
          <a href="#" class="nav-item dropdown-item">You have 5 more tasks</a>
        </li>
        <li class="nav-link">
          <a href="#" class="nav-item dropdown-item"
            >Your friend Michael is in town</a
          >
        </li>
        <li class="nav-link">
          <a href="#" class="nav-item dropdown-item">Another notification</a>
        </li>
        <li class="nav-link">
          <a href="#" class="nav-item dropdown-item">Another one</a>
        </li>
      </base-dropdown> -->
      <div v-if="account.loggedIn" class="nav-item">
        <p style="margin-top:8px">Logged in as: {{ account.username }}</p>
      </div>
      <base-dropdown
        tag="li"
        :menu-on-right="!$rtl.isRTL"
        title-tag="a"
        class="nav-item"
        title-classes="nav-link"
        menu-classes="dropdown-navbar"
      >
        <template slot="title">
          <div class="photo"><i class="tim-icons icon-single-02"></i></div>
          <b class="caret d-none d-lg-block d-xl-block"></b>
          <p class="d-lg-none">Log in</p>
        </template>
        <!-- <li class="nav-link">
          <a href="#" class="nav-item dropdown-item">Profile</a>
        </li>
        <li class="nav-link">
          <a href="#" class="nav-item dropdown-item">Settings</a>
        </li>
        <div class="dropdown-divider"></div> -->
        <li class="nav-link" v-if="!account.loggedIn">
          <button @click="toggleLoginModal" class="nav-item dropdown-item">
            Log in
          </button>
        </li>
        <li class="nav-link" v-if="!account.loggedIn">
          <button @click="toggleRegisterModal" class="nav-item dropdown-item">
            Register
          </button>
        </li>
        <li class="nav-link" v-if="account.loggedIn">
          <p class="text-muted">Current user: {{ account.username }}</p>
          <button @click="logout" class="nav-item dropdown-item">
            Log out
          </button>
        </li>
      </base-dropdown>
      <modal
        :show.sync="account.loginModalVisible"
        class="modal-black"
        id="loginModal"
        :centered="true"
        :show-close="true"
      >
        <h2 slot="header" type="text" id="LoginTitle">
          Login
        </h2>
        <h4
          v-if="account.wrongPassword"
          type="text"
          id="wrongPasswordMessage"
          class="text-warning"
        >
          Username or password does not exist.
        </h4>
        <h4
          v-if="account.userCreatedMessage"
          type="text"
          id="userCreatedMessage"
          class="text-success"
        >
          Account created, please log in!
        </h4>
        <form @submit="loginSubmitted">
          <label v-if="account.missingLoginInfo" class="text-warning"
            >Username (needed):</label
          >
          <label v-if="!account.missingLoginInfo" class="text-primary"
            >Username:</label
          >
          <input
            type="username"
            v-model="account.username"
            class="form-control"
            id="usernameInput"
            placeholder="Username"
          />
          <label v-if="account.missingLoginInfo" class="text-warning"
            >Password (needed):</label
          >
          <label v-if="!account.missingLoginInfo" class="text-primary"
            >Password:</label
          >
          <input
            type="password"
            v-model="account.password"
            class="form-control"
            id="passwordInput"
            placeholder="Password"
          />
          <input
            type="submit"
            value="Login"
            class="btn-primary"
            style="margin-top:8pt"
          />
        </form>
        <div slot="footer">
          <a @click="toggleRegisterModal" class="text-info">
            No account? Register here!
          </a>
        </div>
      </modal>
      <modal
        :show.sync="account.registerModalVisible"
        class="modal-black"
        id="registerModal"
        :centered="true"
        :show-close="true"
      >
        <h2 slot="header" type="text" id="RegisterTitle">
          Register new account
        </h2>
        <h4
          v-if="account.registerFail"
          type="text"
          id="registerFailMessage"
          class="text-warning"
        >
          Username exists, choose another one or log in.
        </h4>
        <form @submit="registerSubmitted">
          <label v-if="account.missingLoginInfo" class="text-warning"
            >Username (needed):</label
          >
          <label v-if="!account.missingLoginInfo" class="text-primary"
            >Username:</label
          >
          <input
            type="username"
            v-model="account.username"
            class="form-control"
            id="registerUsernameInput"
            placeholder="Username"
          />
          <label v-if="account.missingLoginInfo" class="text-warning"
            >Password (needed):</label
          >
          <label v-if="!account.missingLoginInfo" class="text-primary"
            >Password:</label
          >
          <input
            type="password"
            v-model="account.password"
            class="form-control"
            id="registerPasswordInput"
            placeholder="Password"
          />
          <input
            type="submit"
            value="Register"
            class="btn-primary"
            style="margin-top:8pt"
          />
        </form>
        <div slot="footer">
          <a @click="toggleLoginModal" class="text-info">
            Already have an account? Login here!
          </a>
        </div>
      </modal>
    </ul>
    <modal
      :show.sync="account.logoutModalVisible"
      class="modal-success"
      id="logoutModal"
      :centered="false"
      :show-close="true"
    >
      <h2 slot="header" type="text" id="logoutTitle">
        Logout successful!
      </h2>
    </modal>
  </base-nav>
</template>
<script>
import { CollapseTransition } from "vue2-transitions";
import { BaseNav, Modal } from "@/components";
import BaseInput from "../Inputs/BaseInput.vue";

const crypto = require("crypto");

export default {
  components: {
    CollapseTransition,
    BaseNav,
    Modal,
    BaseInput,
  },
  computed: {
    routeName() {
      const { path } = this.$route;
      let parts = path.split("/");
      if (parts == ",") {
        return "Map";
      }
      return parts.map((p) => this.capitalizeFirstLetter(p)).join(" ");
    },
    isRTL() {
      return this.$rtl.isRTL;
    },
  },
  data() {
    return {
      activeNotifications: false,
      showMenu: false,
      searchModalVisible: false,
      searchQuery: "",
      account: {
        loginModalVisible: false,
        registerModalVisible: false,
        logoutModalVisible: false,
        userCreatedMessage: false,
        username: "",
        password: "",
        missingLoginInfo: false,
        loggedIn: false,
        wrongPassword: false,
        registerFail: false,
      },
    };
  },
  methods: {
    capitalizeFirstLetter(string) {
      if (!string || typeof string !== "string") {
        return "";
      }
      return string.charAt(0).toUpperCase() + string.slice(1);
    },
    closeDropDown() {
      this.activeNotifications = false;
    },
    toggleSidebar() {
      this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
    },
    toggleMenu() {
      this.showMenu = !this.showMenu;
    },
    toggleLoginModal() {
      this.account.loginModalVisible = true;
      this.account.registerModalVisible = false;
      this.account.missingLoginInfo = false;
      this.account.wrongPassword = false
      // console.log("loginModalVisible:", this.loginModalVisible);
      // console.log("registerModalVisible", this.registerModalVisible);
    },
    toggleRegisterModal() {
      this.account.registerModalVisible = true;
      this.account.loginModalVisible = false;
      this.account.missingLoginInfo = false;
      // console.log("registerModalVisible", this.registerModalVisible);
      // console.log("loginModalVisible:", this.loginModalVisible);
    },
    async loginSubmitted(e) {
      e.preventDefault();
      console.log("login submit");
      if (!this.account.username || !this.account.password) {
        this.account.missingLoginInfo = true;
        return;
      }
      const hashedPassword = crypto
        .createHash("sha1")
        .update(this.account.password)
        .digest("hex");
      // console.log(this.username);
      // console.log(this.password);
      this.account.password = "";

      const loginResponse = await this.$axios.post("/api/authenticate", {
        username: this.account.username,
        password: hashedPassword,
      });

      console.log(loginResponse.data);

      if (loginResponse.data.access) {
        console.log("authentication success");
        this.account.loggedIn = true;
        this.account.wrongPassword = false;
        this.account.loginModalVisible = false;
        this.$store.commit('setCity',loginResponse.data.lastSearch)
        console.log(this.$store.state.lastCity)
      } else {
        this.account.wrongPassword = true;
        this.account.userCreatedMessage = false;
        console.log("authentication failed");
      }
    },
    async registerSubmitted(e) {
      e.preventDefault();
      console.log("register submit");
      if (!this.account.username || !this.account.password) {
        this.account.missingLoginInfo = true;
        return;
      }
      const hashedPassword = crypto //hashing password before sending.
        .createHash("sha1")
        .update(this.account.password)
        .digest("hex");
      // console.log(this.username);
      // console.log(this.password);

      const registerResponse = await this.$axios.post("/api/register", {
        username: this.account.username,
        password: hashedPassword,
      });

      console.log(registerResponse.data);
      this.account.password = ""; //Clearing password from the browser
      console.log(registerResponse.data.register);
      if (registerResponse.data.register) {
        this.account.userCreatedMessage = true;
        this.account.registerFail = false;
        this.account.registerModalVisible = false;
        this.account.loginModalVisible = true;
        this.account.wrongPassword = false;

        console.log(this.userCreatedModalVisible);
      } else {
        this.account.registerFail = true;
        this.account.userCreatedMessage = false;
      }
    },
    async logout() {
      this.account.loggedIn = false;


      const lastsearch = this.$store.state.lastCity;
      console.log(lastsearch);

      const logoutResponse = await this.$axios.post("/api/logout", {
        username: this.account.username,
        lastsearch: lastsearch,
      });
      console.log(logoutResponse.data);

      this.resetModals()
      this.account.logoutModalVisible = true;
      console.log(this.account.logoutModalVisible);

      //send last search to backend
    },
    resetModals() {
      this.account.loginModalVisible = false;
      this.account.registerModalVisible = false;
      this.account.logoutModalVisible = false;
      this.account.userCreatedMessage = false;
      this.account.username = "";
      this.account.password = "";
      this.account.missingLoginInfo = false;
      this.account.loggedIn = false;
      this.account.wrongPassword = false;
      this.account.registerFail = false;
    },
  },
};
</script>
<style scoped>
.top-navbar {
  top: 0px;
}
</style>
