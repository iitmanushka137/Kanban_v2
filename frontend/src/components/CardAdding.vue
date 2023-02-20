<template>
    <div class="cardadd" style="position:relative; min-height: 100vh; margin: 0px; background: linear-gradient(to bottom, #DCBF0A 0%, #3B3303 100%);">
        <div align="middle">
            <p class="alert alert-danger" v-if="error">{{ error }}</p>
        </div>
        <div align="right" style="color: black">
            <router-link :to="`/home`">
                <button style="height: 30px; width: 90px; border: 1px solid black; color: black">Home</button>
            </router-link> | 
            <button @click="exportLists" style="height: 30px; width: 90px; border: 1px solid black; color: black">Export</button> |
            <router-link :to="`/summary`">
                <button style="height: 30px; width: 90px; border: 1px solid black; color: black">Summary</button>
            </router-link> |
            <router-link :to="`/`">
                <button @click="clean" style="height: 30px; width: 90px; border: 1px solid black; color: black">Logout</button>
            </router-link>
        </div>
        <div align="middle" style="left:460px; top: 40px; position: absolute; margin: 60px; box-shadow:10px 10px 15px 15px #FAF136; background: wheat">
        <h3 align="center" style="color: black">Add Card</h3>
        <div class="container" style="font-size: 1.5rem; display: inline-block; margin: 10px 50px 20px;">
        <div>
            <label style="color: black">List</label>&nbsp;
            <select class="form-select" v-model="nlid">
                <option v-for="option in this.lists" :key="option.list_id" :value="option.list_id">
                {{ option.list_name }}
                </option>
            </select>
        </div>
        <div class="row" style="position: relative; margin: 50px 48px 50px;">
            <label style="color: black"><strong>Card Name </strong></label>
            <input type="text" v-model="cname" name="cname" placeholder="Please enter card name" style="height: 20px" required/>
        </div>
        <div class="row" style="position: relative; margin: 50px 48px 50px;">
            <label style="color: black"><strong>Card Content </strong></label>
            <input type="text" v-model="ccont" name="ccont" placeholder="Please enter card content" style="height: 20px" required/>
        </div>
        <div class="row" style="position: relative; margin: 50px 48px 50px;">
            <label style="color: black"><strong>Deadline Date </strong></label>
            <input type="date" v-model="dd" name="dd" style="height: 20px" required/>
        </div>
        <div class="row" style="position: relative; margin: 50px 48px 50px;">
            <label style="color: black"><strong>Mark as complete </strong></label>
            <input type="checkbox" v-model="compd" name = "compd" style="height: 20px"/>
        </div>
        </div>
        <div class="row" style="margin: 10px 48px 20px;"></div>
        <router-link :to="`/home`">
            <button style="padding: 14px 40px; background-color: white; color: black; border: 2px solid black; border-radius: 50%; margin: 10px 48px 20px;" type="submit" @click="addCard">Add Card</button>
        </router-link>
    </div>
    </div>
</template>
<script>
    export default {
        name: 'CardAdding',
        data() {
            return {
                email: null,
                auth_token: null,
                lists: [],
                error: "",
                lid: null,
                nlid: null,
                cname: null,
                ccont: null,
                dd: null,
                compd: null
            };
        },
        async created() {
            this.email=sessionStorage.getItem("email");
            this.auth_token=sessionStorage.getItem("auth-token");
            if(!this.auth_token){
                alert("Login to view your Dashboard")
                this.$router.push("/")
            }
            this.lid=localStorage.getItem("lid");
            this.lists=localStorage.getItem("lists")
            return fetch(`http://127.0.0.1:5000/api/list/${this.email}`,{
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": `${this.auth_token}`
                }
            }).then((response) => response.json())
            .then((data) => {
                this.lists = data
                console.log(data)
                localStorage.setItem("lists", this.lists)
            }).catch((error) => console.log("1st", error))
        },
        methods: {
            async clean() {
                sessionStorage.clear()
                localStorage.clear()
            },
            async addCard() {
                if(!this.cname || !this.ccont || !this.dd) {
                    this.error = "Card Name or Card Content and Deadline date can't be empty";
                }
                else {
                    if(this.lid!=this.nlid && this.nlid) {
                        this.lid=this.nlid
                        localStorage.setItem("lid", this.lid)
                    }
                    try {
                        fetch(`http://127.0.0.1:5000/api/card/${this.email}/${this.lid}`, {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json;charset=utf-8",
                                "Authentication-Token": `${this.auth_token}`,
                            },
                            body: JSON.stringify({
                                email: this.email,      
                                card_name : this.cname,
                                card_content: this.ccont,
                                deadline_date: this.dd,
                                completion_date: this.compd,
                                lid: this.lid
                            }),
                        })
                        .then((resp) =>  resp.json())
                        .then((data) => {
                            const response = data;
                            if (response.message) {
                                this.error = response.message;
                                console.log(response.message);
                            } else {
                                this.c = data;
                                console.log(this.c);
                                console.log("Card Added");
                                this.$router.go("home");
                                console.log("its dashboard returns");
                            }
                        })
                        .catch((error) => {
                            console.log("1st",error);
                        });
                    } catch (error) {
                        console.log("2nd",error);
                    }
                }
            }
        }
    }
</script>