<template>
	<view>
		<view class="model">
			<navigator hover-class="none" v-for="(item,index) in model" :key="index" class="model-item" :style="{backgroundColor: item.color}"
			 :url="item.name=='匿名表白墙'?'../anouym/anouym?model_id='+item.id:'../model_detail/model_detail?model_id='+item.id">
				<view style="margin-top: 25upx;">
					<image :src="item.src" mode="widthFix"></image>
				</view>
				<text style="margin-top: 5upx;font-size: 16px">{{item.name}}</text>
			</navigator>
		</view>
		<view class="hot-topic" v-for="(item_model,index_model) in model" :key="index_model">
			<navigator hover-class="none" class="header" :style="{borderLeftColor: item_model.color}" :url="item_model.name=='匿名表白墙'?'../anouym/anouym?model_id='+item_model.id:'../model_detail/model_detail?model_id='+item_model.id">
				<text style="font-size: 15px">{{item_model.name}}</text>
				<view class="all">
					<view>更多话题</view>
					<image src="../../static/img/right.png"></image>
				</view>
			</navigator>
			<view class="tip" v-if="item_model.topic.length===0">当前版块还没有任何话题哦！</view>


			<navigator v-if="item_model.name!='匿名表白墙'" hover-class="none" :url="'../topic_detail/topic_detail?topic_id='+item.id"
			 :class="{top_border:index_topic!==0}" class="hot-topic-item" v-for="(item, index_topic) in item_model.topic" :key="index_topic">
				<view class="head_image">
					<image :src="item.publisher_info.user_image" mode="aspectFill"></image>
				</view>
				<view class="content">
					<view class="topic-item-header">
						<view class="publish_info">
							<view style="font-size: 16px;color: #414141;" class="name">
								<view>{{item.publisher_info.name}}</view>
								<image :src="gender_list[item.publisher_info.gender]"></image>
							</view>
							<view style="font-size: 12px;color: #999">{{item.publish_date}}</view>
						</view>
						<view class="counts">
							<view class="in_counts">
								<image src="../../static/img/great.png"></image>
								<view> {{item.great_counts}}</view>
							</view>
							<view class="in_counts">
								<image src="../../static/img/comment.png"></image>
								<view> {{item.comment_counts}}</view>
							</view>
						</view>
					</view>
					<view class="topic-item-footer">
						{{item.title}}
					</view>
				</view>
			</navigator>

			<!-- 表白墙版块 -->
			<navigator v-if="item_model.name=='匿名表白墙'" hover-class="none" :url="'../anouym_detail/anouym_detail?topic_id='+item.id"
			 :class="{top_border:index_topic!==0}" class="hot-topic-item" v-for="(item, index_topic) in item_model.topic" :key="index_topic">
				<view class="head_image">
					<image src="../../static/img/anouym.png" mode="aspectFill"></image>
				</view>
				<view class="content">
					<view class="topic-item-header">
						<view class="publish_info">
							<view style="font-size: 16px;color: #414141;" class="name">
								<view>匿名用户</view>
								<image :src="gender_list[item.publisher_info.gender]"></image>
							</view>
							<view style="font-size: 12px;color: #999">{{item.publish_date}}</view>
						</view>
						<view class="counts">
							<view class="in_counts">
								<image src="../../static/img/great.png"></image>
								<view> {{item.great_counts}}</view>
							</view>
							<view class="in_counts">
								<image src="../../static/img/comment.png"></image>
								<view> {{item.comment_counts}}</view>
							</view>
						</view>
					</view>
					<view class="topic-item-footer">
						{{item.title}}
					</view>
				</view>
			</navigator>
		</view>



		<image src='../../static/img/to_top.png' class='goTop' v-if='floorstatus' @tap="goTop"></image>
		<image src='../../static/img/publish.png' class='goTop' v-if='!floorstatus' @tap.stop="publish"></image>
		<view @tap.stop="show_personal" v-if="!is_show_personal" class="personal_tip">
			<image src="../../static/img/circle.png"></image>
			<!-- <view v-if="user_info.disread_sum>0">{{user_info.disread_sum}}</view> -->
		</view>

		<!--个人中心-->
		<view v-if="is_show_personal" class="personal_">
			<view class="personal">
				<view class="head">
					<image :src="user_info.user_image" mode="aspectFill" @tap="change_head_image"></image>
					<text>{{user_info.name}}</text>
				</view>
				<navigator hover-class="none" style="font-size:14px" url="../school_confirm/school_confirm" class="weui-cell weui-cell_access">
					<image src="../../static/img/link_to_school.png"></image>
					<view class="weui-cell__bd">{{!user_info.true_name||user_info.true_name.length===0?'绑定':'换绑'}}教务系统</view>
					<view class="weui-cell__ft weui-cell__ft_in-access"></view>
				</navigator>
				<navigator hover-class="none" style="font-size:14px" v-for="(item, index) in list" :key="index" :url="item.url"
				 class="weui-cell weui-cell_access">
					<image :src="item.src"></image>
					<view class="weui-cell__bd">{{item.title}}</view>
					<view v-if="index===4&&user_info.disread_sum>0" class="disread">
						<view class="num">
							{{user_info.disread_sum}}
						</view>
					</view>
					<view class="weui-cell__ft weui-cell__ft_in-access"></view>
				</navigator>
				<navigator hover-class="none" style="font-size:14px; border-bottom: #ddd 1px solid" url="../about_app/about_app"
				 class="weui-cell weui-cell_access">
					<image src="../../static/img/feedback.png"></image>
					<view class="weui-cell__bd">关于技大论坛</view>
					<view class="weui-cell__ft weui-cell__ft_in-access"></view>
				</navigator>

				<image src="../../static/img/left.png" class="back" @tap.stop="show_personal"></image>
			</view>
			<view class="space" @tap.stop="show_personal"></view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				inputShowed: false,
				inputVal: "",
				model: uni.getStorageSync('index_data') || [],
				floorstatus: false,
				is_show_personal: false,
				user_info: getApp().globalData.user_info,
				list: [{
						title: '个人信息',
						url: '../user_info/user_info',
						src: '../../static/img/user_info.png'
					},
					{
						title: '我的话题',
						url: '../my_publish/my_publish',
						src: '../../static/img/publish.png'
					},
					{
						title: '我赞过的话题',
						url: '../my_like_topic/my_like_topic',
						src: '../../static/img/my_like.png'
					},
					{
						title: '我评论的话题',
						url: '../my_comment_topic/my_comment_topic',
						src: '../../static/img/my_comment.png'
					},
					{
						title: '与我相关',
						url: '../link_to_me/link_to_me',
						src: '../../static/img/link_to_me.png'
					},
					{
						title: '用户协议',
						url: '../announce/announce',
						src: '../../static/img/agreement.png'
					},
				],
				gender_list: ['', '../../static/img/boy.png', '../../static/img/girl.png'],
				apk_url: ''
			}
		},
		methods: {
			publish: function() {
				if (this.user_info.true_name && this.user_info.true_name.length > 0) {
					uni.navigateTo({
						url: '../publish/publish'
					})
				} else {
					uni.showModal({
						title: '提示',
						content: '请先绑定教务系统',
						showCancel: false,
						success(res) {
							if (res.confirm) {
								uni.navigateTo({
									url: '../register0/register0'
								})
							}
						}
					})
				}
			},
			show_personal: function() {
				this.is_show_personal = !this.is_show_personal
			},
			goTop: function(e) { // 一键回到顶部
				if (uni.pageScrollTo) {
					uni.pageScrollTo({
						scrollTop: 0
					})
				} else {
					uni.showModal({
						title: '提示',
						content: '当前微信版本过低，无法使用该功能，请升级到最新微信版本后重试。'
					})
				}
			},
			change_head_image() {
				var that = this
				uni.chooseImage({
					count: 1,
					sizeType: ['compressed'],
					sourceType: ['album', 'camera'],
					success(res) {
						// tempFilePath可以作为img标签的src属性显示图片
						const tempFilePaths = res.tempFilePaths //返回一个url数组
						uni.uploadFile({
							url: getApp().globalData.host+'user/register_head_image/',
							filePath: tempFilePaths[0],
							name: 'file',
							formData: {
								user_id: getApp().globalData.user_info.id
							},
							success(res) {
								getApp().globalData.user_info = JSON.parse(res.data).user_info
								that.user_info = JSON.parse(res.data).user_info
								uni.setStorageSync('user_info', JSON.parse(res.data).user_info)
								uni.showModal({
									showCancel: false,
									title: '提示',
									content: '修改头像成功',
								})
							}
						})
					}
				})
			}
		},
		onLoad: function(e) {
			if (e.token === 'sztubbs') {
				var that = this
				uni.request({
					url: getApp().globalData.host+'user/get_info/',
					data: {
						token: getApp().globalData.token,
						id: e.id
					},
					success(res) {
						console.log(res)
						if (res.statusCode === 200) {
							console.log(res)
							getApp().globalData.user_info = res.data
							that.user_info = res.data
							uni.setStorageSync('user_info', res.data)
						} else {
							console.log(res)
							uni.showToast({
								title: '服务器连接失败',
								icon: "none"
							})
						}
					},
				})
				getApp().globalData.user_info = uni.getStorageSync('user_info')
				this.user_info = getApp().globalData.user_info
				uni.request({
					url: getApp().globalData.host+'article/get_index0_data/',
					data: {
						token: getApp().globalData.token
					},
					success: (res) => {
						// console.log(res)
						that.model = res.data.model
					}
				})
				// console.log('缓存数据')
				// console.log(uni.getStorageSync('user_info'))
				// if (getApp().globalData.user_info.name.length === 0) {
				// 	// console.log('执行了index的onload')
				// 	uni.redirectTo({
				// 		url: '../register/register'
				// 	})
				// }
			}
		},
		onPageScroll: function(e) {
			this.floorstatus = e.scrollTop > 100;
		},
		onPullDownRefresh: function() {
			// 标题栏显示刷新图标，转圈圈
			// uni.showNavigationBarLoading()
			// 请求最新数据
			var that = this
			uni.request({
				url: getApp().globalData.host+'article/get_index0_data/',
				success(res) {
					if (res.statusCode === 200) {
						console.log(res)
						that.model = res.data.model
						uni.showToast({
							title: '刷新成功',
							icon: 'success',
							duration: 500
						})
						uni.stopPullDownRefresh()
						// uni.hideNavigationBarLoading()
					} else {
						uni.showToast({
							title: '服务器连接失败',
							icon: "none"
						})
						uni.stopPullDownRefresh()
						// uni.hideNavigationBarLoading()
					}
				},
				fail(res) {
					uni.showToast({
						title: '网络异常',
						icon: "none"
					})
				}
			})
			uni.request({
				url: getApp().globalData.host+'user/get_info/',
				data: {
					token: getApp().globalData.token,
					id: getApp().globalData.user_info.id
				},
				success(res) {
					console.log(res)
					if (res.statusCode === 200) {
						console.log(res)
						getApp().globalData.user_info = res.data
						that.user_info = res.data
						uni.setStorageSync('user_info', res.data)
					} else {
						console.log(res)
						uni.showToast({
							title: '服务器连接失败',
							icon: "none"
						})
					}
				},
				fail(res) {
					uni.showToast({
						title: '网络异常',
						icon: "none"
					})
				}
			})
			// uni.hideNavigationBarLoading()
		},
		onHide() {
			wx.setStorageSync('index_data', this.model)
		},
		onShow() {
			this.user_info = getApp().globalData.user_info
		}
	}
</script>

<style>
	@import 'index.css';
</style>
