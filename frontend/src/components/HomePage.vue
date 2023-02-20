<template>
  <div class="home">
    <p align="middle" class="alert alert-danger" v-if="error">{{ error }}</p>
    <p align="middle" class="alert alert-success" v-if="good">{{ good }}</p>
    <div align="right">
      <button @click="exportLists" style="height: 30px; width: 90px; border: 1px solid black; color: black">Export</button> |
      <router-link :to="`/summary`">
        <button style="height: 30px; width: 90px; border: 1px solid black; color: black">Summary</button>
      </router-link> |
      <router-link :to="`/`">
        <button @click="clean" style="height: 30px; width: 90px; border: 1px solid black; color: black">Logout</button>
      </router-link>
    </div>
    <h3 align="left">Welcome {{ this.username.username }}</h3>
      <div v-if="lists" style="border: 3px solid blue; position: relative; display: flex; flex-wrap:wrap; background: wheat">
          <div align="middle" v-for="(value, index) in lists" :key="index" style = "color:#fff; border:3px solid black; box-shadow: 10px 10px 15px 15px grey; width:350px; display: inline-block; min-height: 250px; margin: 45px 48px 30px; padding: 10px; background: linear-gradient(to bottom, #199895 0%, #01EDF9 100%);">
            <p style = "border:3px solid black; color: black"><strong>  {{ value.list_name }}</strong> &nbsp; 
              <router-link :to="`/updateList/${value.list_id}`">
                <button @click="storeID(value.list_id); storeData(value.list_name, value.list_description)" style="height: 30px; width: 90px; border: 1px solid black; color: blue">Update</button>
              </router-link>&nbsp;
              <router-link :to="`/delList/${value.list_id}`">
                <button @click="storeID(value.list_id)" style="height: 30px; width: 90px; border: 1px solid black; color: blue">Delete</button>
              </router-link>
            </p>
            <div v-if="cards">
              <div v-for="(value_, index_) in cards" :key="index_">
                <div v-if="value.list_id==index_">
                  <div v-for="c in value_" :key="c.card_id">
                    <div class="row" style = "border:3px solid black; background: transparent;">
                      <p style="border:3px solid black; color: black"><strong>{{ c.card_name }} </strong>&nbsp;
                        <router-link :to="`/updateCard/${c.card_id}`"> 
                          <button @click="storeLID(value.list_id); storeCID(c.card_id); storeCData(c.card_name, c.card_content, c.deadline_date, c.completion_date)" style="height: 28px; width: 80px; border: 1px solid black; color: blue">Update</button>
                        </router-link>&nbsp;
                        <router-link :to="`/delCard/${c.card_id}`">
                          <button @click="storeCID(c.card_id)" style="height: 25px; width: 80px; border: 1px solid black; color: blue">Delete</button>
                        </router-link>
                      </p>
                      <p align="left"> Created Date <strong>{{ c.created_date }}</strong></p>
                      <p align="center">{{ c.card_content }}</p>
                      <p align = "right">Deadline <strong> {{ c.deadline_date }}</strong></p>
                      <div v-if="c.completed_date=='None'">
                        <p align="center" style="color: black"><strong>Incomplete</strong></p> 
                      </div>
                      <div v-else>
                        <p align="center">Completed Date <strong>{{ c.completed_date }}</strong></p>
                        <p align="center" style="color: black"><strong>Complete</strong></p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="row">
              <p>
                <router-link :to="`/addcard/${value.list_id}`">
                  <button @click="storeLID(value.list_id)" style="height: 20px; width: 80px; border: 1px solid black; color: red">Add Card</button>
                </router-link>
              </p>
              <button @click="storeLID(value.list_id); exportCards()" style="height: 20px; width: 80px; border: 1px solid black; color: red">Export</button>
            </div>
        </div>
    </div>
    <div align="middle" style="margin: 20px;">
      <strong><a href="/addlist"><button style="height: 70px; width: 150px; font-size: 1.5rem; border: 2px solid black; color: red">+ Add List</button></a></strong>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  data() {
    return {
      username: {},
      listid: null,
      email: null,
      auth_token: null,
      lists: {},
      cards: {},
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
    return fetch(`http://127.0.0.1:5000/api/card/${this.email}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": `${this.auth_token}`
      }
    }).then((response) => response.json())
    .then((data) => {
      this.username=data[0]
      this.lists = data[1]
      this.cards = data[2]
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
    async storeLID(lid) {
      localStorage.setItem("lid", lid)
    },
    storeCID(cid) {
      localStorage.setItem("cid", cid)
    },
    storeCData(cname, ccont, dd, compd) {
      localStorage.setItem("cname", cname),
      localStorage.setItem("ccont", ccont)
      localStorage.setItem("dd", dd)
      localStorage.setItem("compd", compd)
    },
    async exportLists(){
      this.email = sessionStorage.getItem("email")
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
    },
    async exportCards() {
      this.lid=localStorage.getItem("lid")
      this.email=sessionStorage.getItem("email")
      return fetch(`http://127.0.0.1:5000/api/exportCard/${this.email}/${this.lid}`,{
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
