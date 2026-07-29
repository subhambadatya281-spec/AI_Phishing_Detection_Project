import joblib
import matplotlib.pyplot as plt
import pandas as pd

model = joblib.load("models/phishing_model.pkl")

columns = [
    'NumDots','SubdomainLevel','PathLevel','UrlLength','NumDash',
    'NumDashInHostname','AtSymbol','TildeSymbol','NumUnderscore',
    'NumPercent','NumQueryComponents','NumAmpersand','NumHash',
    'NumNumericChars','NoHttps','RandomString','IpAddress',
    'DomainInSubdomains','DomainInPaths','HttpsInHostname',
    'HostnameLength','PathLength','QueryLength',
    'DoubleSlashInPath','NumSensitiveWords','EmbeddedBrandName',
    'PctExtHyperlinks','PctExtResourceUrls','ExtFavicon',
    'InsecureForms','RelativeFormAction','ExtFormAction',
    'AbnormalFormAction','PctNullSelfRedirectHyperlinks',
    'FrequentDomainNameMismatch','FakeLinkInStatusBar',
    'RightClickDisabled','PopUpWindow','SubmitInfoToEmail',
    'IframeOrFrame','MissingTitle','ImagesOnlyInForm',
    'SubdomainLevelRT','UrlLengthRT','PctExtResourceUrlsRT',
    'AbnormalExtFormActionR','ExtMetaScriptLinkRT',
    'PctExtNullSelfRedirectHyperlinksRT'
]

importance = model.feature_importances_

df = pd.DataFrame({
    "Feature": columns,
    "Importance": importance
})

df = df.sort_values(
    by="Importance",
    ascending=False
).head(15)

plt.figure(figsize=(10,6))
plt.barh(df["Feature"], df["Importance"])
plt.title("Top 15 Important Features")
plt.tight_layout()

plt.savefig(
    "static/feature_importance.png",
    bbox_inches="tight"
)

plt.close()

print("Feature Importance Graph Saved")