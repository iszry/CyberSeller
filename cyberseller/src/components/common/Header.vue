<template>
  <div class="header">
    <!-- 前往主页按钮 -->
    <router-link to="/" style="color: #F2F8FE">

      <div class="logo" style="position: absolute;">
        <div class="collapse-btn">
          <i class="el-icon-s-home"></i>
        </div>
        <!-- <img style="width: 70px;height: 50px;margin-top: 10px;" src="../../assets/img/logo.png"> -->
      </div>
<!--      <div class="logo"><img src="../../assets/img/logo.png"></div>-->

    </router-link>

    <div class="header-right">
      <div class="header-user-con">
<!--        &lt;!&ndash; 全屏显示 &ndash;&gt;-->
<!--        <div class="btn-fullscreen" @click="handleFullScreen">-->
<!--          <el-tooltip effect="dark" :content="fullscreen?`取消全屏`:`全屏`" placement="bottom">-->
<!--            <i class="el-icon-rank"></i>-->
<!--          </el-tooltip>-->
<!--        </div>-->

        <!-- 我的购物车 -->
        <div class="btn-bell" v-if="login_state()">
          <el-tooltip effect="dark" content="我的购物车" placement="bottom">
            <router-link to="/carts">
              <i class="el-icon-shopping-cart-2"  style="color: #F2F8FE;"></i>
            </router-link>
          </el-tooltip>
        </div>
        <!-- 我的收藏 -->
        <div class="btn-bell" v-if="login_state()">
          <el-tooltip effect="dark" content="我的收藏" placement="bottom">
            <router-link to="/collection">
              <i class="el-icon-star-on" style="color: #F2F8FE;"></i>
            </router-link>
          </el-tooltip>
        </div>

        <!-- 用户名下拉菜单 -->
        <el-dropdown class="user-name" @command="handleCommand">
                    <span class="el-dropdown-link">
                        {{username}}
                        <i class="el-icon-caret-bottom"></i>
                    </span>
          <el-dropdown-menu slot="dropdown">
            <router-link to="/myOrders"><el-dropdown-item v-if="login_state()">我的订单</el-dropdown-item> </router-link>
            <router-link to="/userInfo"><el-dropdown-item v-if="login_state()">我的信息</el-dropdown-item> </router-link>
            <router-link to="/addressMag"><el-dropdown-item v-if="login_state()">地址管理</el-dropdown-item> </router-link>
            <router-link to="/sellGoods"><el-dropdown-item v-if="login_state()">发布商品</el-dropdown-item> </router-link>
            <el-dropdown-item divided command="loginout">{{ loginout_user }}</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        collapse: false,
        fullscreen: false,
        name: 'admin',
        message: 2,
        drawer: false,
      };
    },
    computed: {
      username() {
        let username = localStorage.getItem('username');
        return username ? username : this.name;
      },
      loginout_user() { 
        return this.username == 'admin' ? '登录' : '退出登录';
      }
    },
    methods: {
      login_state() { 
        return this.username != 'admin';
      },
      // 用户名下拉菜单选择事件
      handleCommand(command) {
        if (command == 'loginout') {
          localStorage.removeItem('username');
          this.$router.push('/login');
        }
      },
      // 侧边栏折叠
      collapseChage() {
        this.collapse = !this.collapse;
        bus.$emit('collapse', this.collapse);
      },
      // 全屏事件
      handleFullScreen() {
        let element = document.documentElement;
        if (this.fullscreen) {
          if (document.exitFullscreen) {
            document.exitFullscreen();
          } else if (document.webkitCancelFullScreen) {
            document.webkitCancelFullScreen();
          } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
          } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
          }
        } else {
          if (element.requestFullscreen) {
            element.requestFullscreen();
          } else if (element.webkitRequestFullScreen) {
            element.webkitRequestFullScreen();
          } else if (element.mozRequestFullScreen) {
            element.mozRequestFullScreen();
          } else if (element.msRequestFullscreen) {
            // IE11
            element.msRequestFullscreen();
          }
        }
        this.fullscreen = !this.fullscreen;
      }
    },
    mounted() {
      if (document.body.clientWidth < 1500) {
        this.collapseChage();
      }
    }
  };
</script>
<style scoped>
  .header {
    position: relative;
    box-sizing: border-box;
    width: 100%;
    height: 70px;
    font-size: 22px;
    color: #fff;
  }
  .collapse-btn {
    float: left;
    padding: 0 21px;
    cursor: pointer;
    line-height: 70px;
  }
  .header .logo {
    float: left;
    width: 250px;
    line-height: 70px;
  }
  .header-right {
    float: right;
    padding-right: 50px;
  }
  .header-user-con {
    display: flex;
    height: 70px;
    align-items: center;
  }
  .btn-bell,
  .btn-fullscreen {
    position: relative;
    width: 30px;
    height: 30px;
    text-align: center;
    border-radius: 15px;
    cursor: pointer;
  }
  .btn-bell-badge {
    position: absolute;
    right: 0;
    top: -2px;
    width: 8px;
    height: 8px;
    border-radius: 4px;
    background: #f56c6c;
    color: #fff;
  }
  .btn-bell .el-icon-bell {
    color: #fff;
  }
  .user-name {
    margin-left: 10px;
  }
  .user-avator {
    margin-left: 20px;
  }
  .user-avator img {
    display: block;
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }
  .el-dropdown-link {
    color: #fff;
    cursor: pointer;
  }

</style>
