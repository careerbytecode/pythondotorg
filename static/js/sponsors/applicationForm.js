$(document).ready(function(){
    const SELECTORS = {
        checkboxesContainer: () => $('#benefits_container'),
        costLabel:  () => $("#cost_label"),
        clearFormBtn:  () => $("#clear_form_btn"),
        packageInput:  () => $("input[name=package]"),
        applicationForm:  () => $("#application_form"),
        getPackageInfo: (packageId) => $("#package_benefits_" + packageId),
        getPackageBenefits: (packageId) => SELECTORS.getPackageInfo(packageId).children(),
        benefitsInputs: () => $("input[id^=id_benefits_]"),
        getBenefitLabel: (benefitId) => $('label[benefit_id=' + benefitId + ']'),
        getBenefitInput: (benefitId) => SELECTORS.benefitsInputs().filter('[value=' + benefitId + ']'),
        getBenefitConflicts: (benefitId) => $('#conflicts_with_' + benefitId).children(),
    }


    let cost = 0;


    SELECTORS.clearFormBtn().click(function(){
        SELECTORS.applicationForm().trigger("reset");
        SELECTORS.applicationForm().find("[class=active]").removeClass("active");
        SELECTORS.packageInput().prop("checked", false);
        SELECTORS.checkboxesContainer().find(':checkbox').each(function(){
            $(this).prop('checked', false);
            if ($(this).attr("package_only")) $(this).attr("disabled", true);
        });
        SELECTORS.costLabel().html("");
    });

    SELECTORS.packageInput().change(function(){
      let package = this.value;
      if (package.length == 0) return;

      SELECTORS.costLabel().html("Updating cost...")

      SELECTORS.checkboxesContainer().find(':checkbox').each(function(){
          $(this).prop('checked', false);
          let packageOnlyBenefit = $(this).attr("package_only");
          if (packageOnlyBenefit) $(this).attr("disabled", true);
      });

      let packageInfo = SELECTORS.getPackageInfo(package);
      SELECTORS.getPackageBenefits(package).each(function(){
          let benefit = $(this).html()
          let benefitInput = SELECTORS.getBenefitInput(benefit);
          let packageOnlyBenefit = benefitInput.attr("package_only");
          benefitInput.removeAttr("disabled");
          benefitInput.trigger("click");
      });

      let cost = packageInfo.attr("data-cost");
      SELECTORS.costLabel.html('Sponsorship cost is $' + cost.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + ' USD')
    });

    SELECTORS.benefitsInputs().change(function(){
      let benefit = this.value;
      if (benefit.length == 0) return;
      if (SELECTORS.costLabel.html() != "Updating cost...") {
        let msg = "Please submit your customized sponsorship package application and we'll contact you within 2 business days."
        SELECTORS.costLabel.html(msg);
      }

      let active = SELECTORS.getBenefitInput(benefit).prop("checked");
      if (!active) {
          return;
      } else {
          SELECTORS.getBenefitLabel(benefit).addClass("active");
      }


      SELECTORS.getBenefitConflicts(benefit).each(function(){
          let conflictId = $(this).html();
          let checked = SELECTORS.getBenefitInput(conflictId).prop("checked");
          if (checked){
            conflictCheckbox.trigger("click");
            conflictCheckbox.parent().removeClass("active");
          }
      });
    });

  $(document).tooltip({
    show: { effect: "blind", duration: 0 },
    hide: false
  });
});
