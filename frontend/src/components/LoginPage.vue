<template>
    <div class="login" style="position:relative; min-height: 100vh; margin: 0px; background: linear-gradient(to bottom, #DCBF0A 0%, #3B3303 100%);">
        <div align="middle">
            <p class="alert alert-danger" v-if="error_1">{{ error_1 }}</p>
            <p class="alert alert-danger" v-if="error_2">{{ error_2 }}</p>
        </div>
        <div align="middle" style="left:460px; top: 40px; position: absolute; margin: 60px; box-shadow:10px 10px 15px 15px #FAF136; background: #BFC833">
        <h1 style="color: black;">Kanban</h1>
        <div class="container" style="font-size: 1.5rem; display: inline-block; margin: 10px 50px 20px;">    
            <div class="row" style="position: relative; margin: 50px 48px 50px;">
            <label style="color: black"><strong>Email ID  </strong></label>
            <input type="email" name="email" v-model="email" placeholder="Provide valid email" style="height: 20px" required/>
            </div>
            
            <div class="row" style="position: relative; margin: 50px 48px 50px;">
            <label style="color: black"><strong>Password  </strong></label>
            <input type="password" name="password" v-model="password" minlength="8" placeholder="Provide a valid  password..." title="Password requires atleast 8 characters." pattern=".{8,}" style="height: 20px" required/>
            </div>
        </div>    
        

        <div class="row" style="margin: 10px 48px 20px;"></div>
        <button id="bton" style="padding: 14px 40px; background-color: white; color: red; font-size: 1.5rem; border: 2px solid black; border-radius: 50%;" type="submit" @click="login">Login</button>
        <p style="color: black">
            <strong>Not Registered ?  </strong>
            <router-link to="/register">Register here</router-link>
        </p>
        </div>
    </div>
</template>
<script>
export default {
    name:'LoginPage',
    data() {
        return {
            email: null,
            password: null,
            error_1: "",
            error_2: "",
            auth: null,
            is_authenticated: false
        }
    },
    async created() {
        sessionStorage.clear()
        localStorage.clear()
    },
    async updated() {
        sessionStorage.clear()
        localStorage.clear()
        },
    methods:{
        async login() {
            try {
                fetch("http://127.0.0.1:5000/login?include_auth_token",{
                    method: "POST",
                    headers: {
                        "Access-Control-Allow-Origin": "*",
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        email: this.email, password: this.password, is_authenticated: true
                    })
                }).then((resp) => resp.json())
                .then(async (data) =>{
                    const { response } = data;
                    console.log(data);
                    if (response.errors) {
                        if (response.errors[1]) {
                            this.error_1 = response.errors[1];
                        }
                        this.error_2 = response.errors[0];
                        console.log(this.error_1, this.error_2);
                    } 
                    else {
                        this.auth = response.user.authentication_token;
                        sessionStorage.setItem("auth-token", this.auth);
                        sessionStorage.setItem("email", this.email);
                        this.$router.push("home");
                        console.log("its homepage");
                    }
                })
                .catch((error) => {
                    console.log("some error first time",error)
                })
            } 
            catch(error){
                console.log("No way home: ", error)
            }
        }
    }
}
</script>

