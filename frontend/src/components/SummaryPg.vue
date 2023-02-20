<template>
    <div class="summary">
      <p class="alert alert-danger" v-if="error" align="middle">{{ error }}</p>
      <p class="alert alert-success" v-if="good" align="middle">{{ good }}</p>
      <div align="right">
        <button @click="exportLists" style="height: 30px; width: 90px; border: 1px solid black; color: black">Export</button> |
        <router-link :to="`/home`">
          <button style="height: 30px; width: 90px; border: 1px solid black; color: black">Home</button>
        </router-link> |
        <router-link :to="`/`">
          <button @click="clean" style="height: 30px; width: 90px; border: 1px solid black; color: black">Logout</button>
        </router-link>
      </div>
      <h3 align="left">Welcome {{ this.username.user_name }}</h3>
      <div v-if="lists" style="border: 6px solid black; position: relative; display: flex; flex-wrap:wrap">
          <div v-for="value in lists" :key="value.list_id" class = "col" style = "color:#fff; border:3px solid black; min-height: 250px; margin: 45px 30px 10px; background: linear-gradient(to bottom, #f68fea 0%, #8c91f8 100%);">
            <p align="center" style = "border:3px solid black; color: black"><strong>{{ value.list_name }}</strong> &nbsp;
              <router-link :to="`/updateList/${value.list_id}`" >
                <button @click="storeID(value.list_id); storeData(value.list_name, value.list_description)" style="height: 30px; width: 90px; border: 1px solid black; color: blue">Update</button>
              </router-link>&nbsp;
              <router-link :to="`/delList/${value.list_id}`">
                <button @click="storeID(value.list_id)" style="height: 30px; width: 90px; border: 1px solid black; color: blue">Delete</button>
              </router-link>
            </p>
            <div v-if="stats">
              <div v-for="stat in stats" :key="stat.list_id">
                <div v-if="value.list_id==stat.list_id" align="center">
                  
                  <p>Total Cards: {{ stat.total_cards }}</p>
                  <p>Completed Cards: {{ stat.completed_cards }}</p>
                  <p>Incomplete Cards: {{ stat.incomplete_cards }}</p>
                  <p>Passed Deadline Cards: {{ stat.passed_deadline }}</p>
                  
                </div>
              </div>
            </div>
            <div v-if="graphs">
              <div v-for="(value_, index_) in graphs" :key="index_">
                <div v-if="value.list_id==index_">
                  <img :src="`data:image/png;base64,${value_}`" alt="image not found" />
                </div>
              </div>
            </div>
          </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "SummaryPg",
    data() {
    return {
      username: {},
      email: null,
      auth_token: null,
      lists: {},
      graphs: {},
      stats: {},
      error: "",
      good: ""
    };
  },
  async created() {
    this.auth_token = sessionStorage.getItem("auth-token")
    this.email = sessionStorage.getItem("email")
    console.log(this.email)
    if(!this.auth_token){
      alert("Login to view your Dashboard")
      this.$router.push("/")
    }
    return fetch(`http://127.0.0.1:5000/api/summary/${this.email}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": `${this.auth_token}`
      }
    }).then((response) => response.json())
    .then((data) => {
      this.username=data[0]
      this.lists = data[1]
      this.stats = data[2]
      this.graphs = data[3]
      console.log(data)
    }).catch((error) => console.log("1st", error))
  },
  methods: {
    async clean() {
      sessionStorage.clear()
      localStorage.clear()
    },
    storeID(list_id){
      localStorage.setItem("list_id",list_id)
    },
    storeData(list_name,list_description){
      localStorage.setItem("list_name",list_name)
      localStorage.setItem("list_description",list_description)
    },
    async exportLists(){
      return fetch(`http://127.0.0.1:5000/api/exportList/${this.email}`,{
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": `${this.auth_token}`
      }
    }).then((response) => response.json())
    .then((data) => {
      console.log(data)
      this.good=data
    }).catch((error) => console.log(error))
    }
  }
  };
  </script>
  