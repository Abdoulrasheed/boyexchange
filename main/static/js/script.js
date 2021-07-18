jQuery(function ($) {
  var clipboard = new ClipboardJS(".pn_copy");
  clipboard.on("success", function (e) {
    $(".pn_copy").removeClass("copied");
    $(e.trigger).addClass("copied");
  });
});

jQuery(function ($) {
  $(".javahref").on("click", function () {
    var the_link = $(this).attr("name");
    window.location = the_link;
  });
});

jQuery(function ($) {
  function create_icons() {
    $(".js_icon_left").hide();
    $(".js_icon_left:first").show();

    $(".js_item_left").each(function () {
      var vtype = $(this).attr("data-type");
      $(".js_icon_left_" + vtype).show();
    });

    $(".js_icon_right").hide();
    $(".js_icon_right:first").show();

    $(
      ".js_line_tab.active .js_item_right, #xtt_right_col_html .js_item_right"
    ).each(function () {
      var vtype = $(this).attr("data-type");
      $(".js_icon_right_" + vtype).show();
    });

    if ($(".js_icon_right.active:visible").length == 0) {
      $(".js_item_right").show();
      $(".js_icon_right").removeClass("active");
      $(".js_icon_right:first").addClass("active");
    }
  }

  function go_active_left_col() {
    if ($(".xtt_html_abs").length > 0) {
      if ($(".js_item_left:visible.active").length == 0) {
        $(".js_item_left").removeClass("active");
        $(".js_item_left:visible:first").addClass("active");
      }
      var valid = $(".js_item_left.active").attr("data-id");

      $(".js_line_tab").removeClass("active");
      $("#js_tabnaps_" + valid).addClass("active");
      create_icons();
    }
  }
  go_active_left_col();

  $(document).on("click", ".js_item_left", function () {
    if (!$(this).hasClass("active")) {
      $(".js_item_left").removeClass("active");
      $(this).addClass("active");
      go_active_left_col();
    }
    return false;
  });

  $(document).on("click", ".js_icon_left", function () {
    if (!$(this).hasClass("active")) {
      var vtype = $(this).attr("data-type");
      $(".js_icon_left").removeClass("active");
      $(this).addClass("active");
      if (vtype == 0) {
        $(".js_item_left").show();
      } else {
        $(".js_item_left").hide();
        $(".js_item_left_" + vtype).show();
      }
      go_active_left_col();
    }
    return false;
  });

  $(document).on("click", ".js_icon_right", function () {
    if (!$(this).hasClass("active")) {
      var vtype = $(this).attr("data-type");
      $(".js_icon_right").removeClass("active");
      $(this).addClass("active");
      if (vtype == 0) {
        $(".js_item_right").show();
      } else {
        $(".js_item_right").hide();
        $(".js_item_right_" + vtype).show();
      }
    }
    return false;
  });
});

jQuery(function ($) {
  const exchange = $("#xchange_id").val();
  const token = $('input[name="csrfmiddlewaretoken"]').val();

  function set_pair_price(action, amount) {
    action_opposite = action === "send" ? "receive" : "send";

    $.ajax({
      type: "POST",
      url: "/get_pair_rate/",
      data: {
        amount,
        action,
        exchange,
        csrfmiddlewaretoken: token,
      },
      beforeSend: function () {
        $("#submit").attr("disabled", true);
        $(".h-loader-" + action_opposite).removeAttr("hidden");
      },
      complete: function () {
        $("#submit").removeAttr("disabled");
        $(".h-loader-" + action_opposite).attr("hidden", true);
      },
      error: function (err) {
        console.log(err);
      },
      success: function (data) {
        const val =
          data.name == "NGN"
            ? Number(data.rate).toFixed(8)
            : Number(data.rate).toFixed(2);
        $("#amount_to_" + action_opposite).val(val);
      },
    });
  }

  $(".send_amount").click(function () {
    let amount = $(this).text();
    $("#amount_to_send").val(amount);
    $("#amount_to_send").trigger("pressed", ["send", amount]);
  });

  $(".receive_amount").click(function () {
    let amount = $(this).text();
    $("#amount_to_receive").val(amount);
    $("#amount_to_receive").trigger("pressed", ["receive", amount]);
  });

  $(document).on("keyup", "#amount_to_send", function () {
    let amount = $(this).val();
    $("#amount_to_receive").trigger("pressed", ["send", amount]);
  });

  $(document).on("keyup", "#amount_to_receive", function () {
    let amount = $(this).val();
    $("#amount_to_receive").trigger("pressed", ["receive", amount]);
  });

  $(document).on("pressed", "#amount_to_send", function (e, action, amount) {
    set_pair_price(action, amount);
  });

  $(document).on("pressed", "#amount_to_receive", function (e, action, amount) {
    set_pair_price(action, amount);
  });

  $("#done_transfer").click(function () {
    const trans_id = $("#transaction_id").text();
    $.ajax({
      type: "POST",
      url: "/mark_paid/",
      data: {
        transaction: trans_id,
        csrfmiddlewaretoken: token,
      },
      beforeSend: function () {
        $("#done_transfer").val("Processing, Please wait...");
      },
      complete: function () {
        $("#done_transfer").val("Redirecting...");
      },
      error: function (err) {
        console.log(err);
      },
      success: function (data) {
        $(this).text("I'M DONE");
        window.location.href = "/success/";
      },
    });
  });
});
