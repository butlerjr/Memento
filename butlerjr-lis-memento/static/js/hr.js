/**
 * Created by fayelisifi on 11/11/14.
 */
var main = function() {
	console.log("Javascipt loaded successfully.");

	$(".delete-button").hover(function() {
		// Mouse in
		$(this).addClass("hover-button");

	}, function() {
		// Mouse out
		$(this).removeClass("hover-button");
	});

	$(".occurrences-display").click(function() {
		entityKey = $(this).find(".entity-key").html()
		occurrences = $(this).find(".occurrences").html()
		$("#memento-instances-modal #occurrences").html(occurrences);
		$("#memento-instances-modal input[name=entity_key]").val(entityKey).prop("disabled", false);
	});

	$(".delete-button").click(
			function() {
				name = $(this).find(".name").html();
				entityKey = $(this).find(".entity-key").html();
				$("#delete-confirmation-modal #name").html(name);
				$("#delete-confirmation-modal input[name=entity_key]").val(
						entityKey).prop("disabled", false);
			});

	$(".edit-button").click(
			function() {
				name = $(this).find(".name").html();
				entityKey = $(this).find(".entity-key").html();
				$("#insert-memento-modal .modal-title").html("Edit Memento");
				$("#insert-memento-modal button[type=submit]").html(
						"Edit Memento");
				$("#insert-memento-modal #name").html(name);
				$("#insert-memento-modal input[name=entity_key]")
						.val(entityKey).prop("disabled", false);
			});

	$(".edit-button").hover(function() {
		// Mouse in
		$(this).addClass("hover-button");

	}, function() {
		// Mouse out
		$(this).removeClass("hover-button");
	});
}

$(document).ready(main);