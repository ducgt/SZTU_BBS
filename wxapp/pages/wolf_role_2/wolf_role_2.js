// pages/wolf_role_2/wolf_role_2.js
let app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    role_list: {
      村民: {img: '../../images/CunMing.jpg', introduce: "（好）虽然没有任何能力，却是狼人杀里最厉害的角色，人数众多，可以主导游戏节奏。"},
      狼人: {img: '../../images/LangRen.jpg', introduce: "每天晚上受到自然之力的影响产生异变，化身为狼人，并残忍的杀害一名角色。所有狼人只有统一意见才会暗杀成功。到了白天隐藏在人群之中，误导其他人的思维，直至取得游戏胜利。狼人最大的武器并不是尖锐的利爪，而是狼人们团结一致的心!"},
      白狼王: {img: '../../images/BaiLangWang.jpg', introduce: "（坏）白天发言阶段可以自爆 并且带走一名玩家 且可以留下来带个刀以后再离场"},
      预言家: {img: '../../images/YuYanJia.jpg', introduce: "（好）村庄中的leader，因为佩戴上古遗物“手形美瞳”，每天晚上可以查验一个人的身份好坏。大部分局中一个预言家的质量往往决定着游戏的走向。如何高效的带领大家走向胜利，何时起跳，如何取信于人，如何存活，都是预言家需要考虑的事情。"},
      女巫: {img: '../../images/NvWu.jpg', introduce: "（好）拥有两瓶药，解药可以救活一名当晚被狼人杀害的玩家，毒药可以毒杀一名玩家，女巫在每天晚上最多使用一瓶药，女巫不可自救。"},
      猎人: {img: '../../images/LieRen.jpg', introduce: "（好）携带一杆猎枪，在自己死亡时，可用仅有的一发子弹射杀任意角色。但如果被女巫毒死(或类似技能)时，则没有时间开枪，只能含冤而死。另外猎人发动技能必翻牌，反之翻牌必须发动技能，不可翻牌后不开枪。"},
      白痴: {img: '../../images/BaiChi.jpg', introduce: "（好）被投票致死的白痴被查出精神病，所以依据本村法律不得判处死刑，翻牌后可继续正常游戏，剥夺投票权利。白痴被投票出局后，在统计游戏胜负结果时可视为死亡，也可视为存活需夜晚再次猎杀，根据游戏人数配置灵活决定"},
      守卫: {img: '../../images/ShouWei.jpg', introduce: "（好）来自瓦肯星的守卫每晚可暗中保护一个角色免受狼人杀害，可以守护自己，但连续两天不可守护同一个人。如果被守护的玩家同时被女巫使用解药(同守同毒)，则该角色依旧死亡。"},
      长老: {img: '../../images/CunZhang.jpg', introduce: "（好）也叫村长，大树，长者。作为村庄里元老级的人物，长者在第一次受到袭击的时候不会死亡，由每名村民贡献一秒的生命使长者继续存活。不过如果长老是被村民误杀的(猎人的子弹，女巫的毒药，村民的投票等)，作为一个莫大的教训，所有的玩家都会失去他们的特殊能力。长老被误杀发动技能建议翻牌，但也可以不翻牌，根据配置灵活决定。"},
      丘比特: {img: '../../images/QiuBiTe.jpg', introduce: "（待定）第一天晚上可以选择射两个人使之成为情侣(可以射自己)，如果其中一人无论因何原因死去，另一个人也会一起殉情而死。当丘比特连接的两个人均为好人时，丘比特归属好人阵营;当丘比特连接一好人一狼时，丘比特及情侣属于第三方阵营，需除掉在场所有人才能取得胜利;当丘比特连接两个狼人时，丘比特算好人阵营"},
      盗贼: {img: '../../images/DaoZei.jpg', introduce: "（待定）在游戏开始时加入额外的两张普通村民卡，在发完身份牌后留下两张牌背面朝上放在桌子上备用。盗贼在第一晚醒来并查看两张卡的内容，就可以选择交换其中一张，然后在之后的游戏中扮演该身份。盗贼可以选择不交换身份，但是如果有狼人牌，则必须交换狼人，如果两张底牌均是狼人牌或两张底牌是一张盗贼牌和一张狼人牌，则重开游戏"},
      警长: {img: '../../images/JingZhang.jpg', introduce: "不属于游戏角色，而是在第一天天亮时在公布死亡讯息前，由玩家投票推举出的一名领导人物，警长有决定发言顺序以及归票的权利，且投票时警长票将当做两票(或1.5票)。当警长死亡时，可选择将警徽移交至任意角色或不移交警徽，让警徽随着警长的死亡逝去。"},
    },
    room_id: 0,
    role: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      room_id: options.room_id
    })
    let that = this
    wx.request({
      url: app.globalData.host+"game/get_user_role/",
      data: {
        room_id: that.data.room_id,
        user_id: app.globalData.user_info.id
      },
      success(res) {
        console.log(res)
        that.setData({
          role: res.data.role
        })
      }
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    let that = this
    wx.request({
      url: app.globalData.host+"game/get_user_role/",
      data: {
        room_id: that.data.room_id,
        user_id: app.globalData.user_info.id
      },
      success(res) {
        console.log(res)
        that.setData({
          role: res.data.role
        })
      }
    })
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})
