<template>
  <div>
    <h2>Регистрация</h2>
    <form @submit.prevent="register">
      <div>
        <label for="registerName">Имя</label>
        <input type="text" id="registerName" v-model="registerName">
      </div>
      <div>
        <label for="registerAge">Возраст</label>
        <input type="text" id="registerAge" v-model="registerAge">
      </div>
      <button>Зарегистрироваться</button>
    </form>
  </div>
  <div>
    <h2>Авторизация</h2>
    <form @submit.prevent="login">
      <div>
        <label for="loginName">Имя</label>
        <input type="text" id="loginName" v-model="loginName">
      </div>
      <button>Авторизоваться</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AuthComponent',
  data() {
    return {
      registerName: '',
      registerAge: '',
      loginName: ''
    }
  },
  methods: {
    async register() {
      const response = await axios.post('http://127.0.0.1:8000/users/', {
        name: this.registerName,
        age: Number(this.registerAge)

      });
      console.log('Register success: ' + response.data)
    },
    async login() {
        const response = await axios.get(`http://127.0.0.1:8000/users/${this.loginName}`)
        if(response.data) {
          this.$emit('handleAuth');
        }else {
          alert("polzovatel ne nayden");
        }
    }
  }
  }
</script>

<style>

</style>
