# Css
styles = """ 
<style>
.c-pill {
	 align-items: center;
	 font-family: "Open Sans", Arial, Verdana, sans-serif;
	 font-weight: bold;
	 font-size: 8px;
	 display: inline-block;
	 height: 100%;
	 white-space: nowrap;
	 width: auto;
	 position: relative;
	 border-radius: 100px;
	 line-height: 1;
	 overflow: hidden;
	 padding: 0px 12px 0px 20px;
	 text-overflow: ellipsis;
	 line-height: 1.25rem;
	 color: #595959;
	 word-break: break-word;
}
 .c-pill:before {
	 border-radius: 50%;
	 content: '';
	 height: 10px;
	 left: 6px;
	 margin-top: -5px;
	 position: absolute;
	 top: 50%;
	 width: 10px;
}

 .c-pill--warning {
	 background: #ffebb6;
}
 .c-pill--warning:before {
	 background: #ffc400;
}

</style>
"""