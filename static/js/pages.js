 (function($){
 	
	$.fn.pages = function(options){
		// PagesClass:"tbody tr", //需要分页的元素
		// 	PagesMth:3, //每页显示个数
		// 	PagesNavMth:5 //显示导航个数
		var opts = $.extend({},$.fn.pages.defaults, options);
		
		return this.each(function(){	
			var $this = $(this);
			var $PagesClass = opts.PagesClass; // 分页元素
			var $AllMth = $this.find($PagesClass).length;  //总个数
			var $Mth = opts.PagesMth; //每页显示个数
			var $NavMth = opts.PagesNavMth; // 导航显示个数
			// 定义分页导航
			var PagesNavHtml = "<div class=\"pag-bar no-pages text-center\"><div class=\"inline middle text-muted\">" +
								"&nbsp;共&nbsp;<span class=\"totalPage\"></span>&nbsp;页&nbsp;&nbsp;&nbsp;</div>" +
								"<ul class=\"pagination middle jp-pag\"><li class=\"jp-first\"><a href=\"javascript:;\">" +
								"首页</a></li><li class=\"jp-previous\">" +
								"<a href=\"javascript:;\">上一页</a></li></ul></div>";
			/*默认初始化显示*/
			$(".pag-bar").remove();
			// $(".pag-bar").css("background-color","red");
			
//			if(1 == 1){
// 如果总个数大于每页显示的个数,不只有一页
				if($AllMth > $Mth){
					// 有多页，就把不显示页码的css去掉
					$(".no-pages").remove();
					// $(".pag-bar").css("border","1px solid red");
					//判断显示
					var relMth = $Mth - 1;//每页个数减1
					$this.find($PagesClass).filter(":gt("+relMth+")").hide();//第1页之后的tr都hide

					// 计算数量,页数
					var PagesMth = Math.ceil($AllMth / $Mth); // 计算页数
					console.log(1111);
					console.log($AllMth);
					console.log($Mth);
					console.log(PagesMth);
					$this.append(PagesNavHtml).find(".totalPage").html(PagesMth);// 共 PagesMth 页
					
					// 计算分页导航显示数量
					var PagesNavNum = "";
					for(var i=1;i<=PagesMth;i++){
						PagesNavNum = PagesNavNum + "<li class=\"jp-paging-item\"><a href=\"javascript:;\">"+i+"</a></li>";
					}
					// 在ul里面先添加页码，在添加“下一页”和“末页”
					$this.find(".pagination").append(PagesNavNum).append("<li class=\"jp-next\"><a href=\"javascript:;\" class=\"PageNext\">下一页</a>" +
					"<li class=\"jp-last\">" +
						"<a href=\"javascript:;\">末页</a>" +
						"</li>").find(".jp-paging-item:first").addClass("active");//页码1高亮

					// console.log($(".jp-paging-item:first").val());
					//每次导航的页码数直显示 （$NavMth） 个，并且禁用上一页和首页
					$this.find(".jp-paging-item").filter(":gt("+($NavMth-1)+")").hide();
					$(".jp-previous, .jp-first").addClass("disabled");
					
				/*默认显示已完成,下面是控制区域代码*/
				
				//导航控制分页
				var $PagesNav = $this.find(".jp-paging-item"); //导航指向
				var $PagesFrist = $this.find(".jp-first"); //首页
				var $PagesLast = $this.find(".jp-last"); //尾页
				var $PagesPrev = $this.find(".jp-previous"); //上一页
				var $PagesNext = $this.find(".jp-next"); //下一页
				
				//导航指向
				$PagesNav.click(function(){
					var NavTxt = $(this).find("a").text();
					showPages(NavTxt);
				});
				//首页
				$PagesFrist.click(function(){
					showPages(1);
				});
				//尾页
				$PagesLast.click(function(){
					showPages(PagesMth);
				});
				//上一页
				$PagesPrev.click(function(){
						
						var OldNav = $this.find(".pagination li.active a");

						if(OldNav.text() == 1){
							$(".jp-previous, .jp-first").addClass("disabled");
						}else{
							var NavTxt = parseInt(OldNav.text()) - 1;
							$(".jp-previous, .jp-first").removeClass("disabled");
							showPages(NavTxt);
						}
					});
				//下一页
				$PagesNext.click(function(){
						
						var OldNav = $this.find(".pagination li.active a");
	
						if(OldNav.text() == PagesMth){
							$(".jp-next, .jp-last").addClass("disabled");
						}else{
							var NavTxt = parseInt(OldNav.text()) + 1;
							$(".jp-next, .jp-last").removeClass("disabled");
							showPages(NavTxt);
						}
				});
			
				// 主体显示隐藏分页函数
				function showPages(page){
					page = parseInt(page);
					
					//页码在最后一页时，下一页和最后一页禁用
					if(page == PagesMth){
						$(".jp-next, .jp-last").addClass("disabled");
					}else{
						if($(".jp-next, .jp-last").hasClass("disabled")){
							$(".jp-next, .jp-last").removeClass("disabled");
						}
					}
					// 页码在第1页时，首页和上一页禁用
					if(page == 1){
						$(".jp-previous, .jp-first").addClass("disabled");
					}else{
						if($(".jp-previous, .jp-first").hasClass("disabled")){
							$(".jp-previous, .jp-first").removeClass("disabled");
						}
					}
					// 当前显示页码高亮（遍历页码）
					$PagesNav.each(function(){
						var NavText = $(this).text();
						if(NavText == page){
							//siblings()找到同胞元素并移除active
							$(this).addClass("active").siblings().removeClass("active");					
						}
					});
					
					//显示导航样式
					if(PagesMth > $NavMth){
						// PagesMth 总页数
						// $NavMth   导航显示个数
						if(page <= ($NavMth/2)){
							// 如果页码在前，就显示前面的页码，隐藏后面的页码，
							$PagesNav.filter(":gt("+($NavMth-1)+")").hide();
							$PagesNav.filter(":lt("+$NavMth+")").show();
						}else if((PagesMth-page) < ($NavMth/2)){
							// 页码在后面
							$PagesNav.filter(":gt("+(PagesMth-$NavMth-1)+")").show();
							$PagesNav.filter(":lt("+(PagesMth-$NavMth)+")").hide();						
						}else{
							var length = parseInt($NavMth/2);
							$PagesNav.hide();
							for(var i=0;i<$NavMth;i++){
								// todo
								$PagesNav.eq(page-length-1+i).show();
							}
						}
					}

					// 显示内容区域
					var LeftPage = $Mth * (page-1);
					var NowPage = $Mth * page;

					$this.find($PagesClass).hide();
					$this.find($PagesClass).filter(":lt("+(NowPage)+")").show();
					$this.find($PagesClass).filter(":lt("+(LeftPage)+")").hide();
				}
			}else{
				$(".pages").html();
			} //判断结束
				
		}); //主体代码
	};
	
	// 默认参数
/*	$.fn.pages.defaults = {
		
		PagesClass:'.item', //需要分页的元素
		PagesMth:4, //每页显示个数		
		PagesNavMth:5 //显示导航个数
	};*/
	
	$.fn.pages.setDefaults = function(settings) {
		$.extend( $.fn.pages.defaults, settings );
	};
	
})(jQuery);